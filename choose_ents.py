import spacy
import textract
import easygui as g
from collections import Counter
import os
import json
import re
import sys


def main(path):

    def ent_labels(doc):
        """Collect lists of ents and their labels.

        :param:
        doc: spacy doc

        :return:
        seen_labels: list
            A list of all ent.label_ found in the text.
        ents: list
            A list of ents found in the text.
        label_index: list
            A list of tuples of the label and the ents belonging to that label.
        """
        seen_labels = []
        ents = []

        # Make a list of all ent types seen in doc
        for ent in doc.ents:
            if ent.label_ not in seen_labels:
                seen_labels.append(ent.label_)
            # Make a list of ents with label and text as tuple
            if not ent.text.isspace():
                ents.append(ent.text)
        seen_labels = list(set(seen_labels))
        label_list = [(ent.label_, ent.text) for ent in doc.ents if not ent.text.isspace()]

        return seen_labels, ents, label_list

    def count_ents(doc):
        """Get total number of occurrences for each ent.text."""

        texts = [ent.text for ent in doc.ents]
        counts = Counter(texts)

        return counts

    def ents_available(redact):
        """Check if there are still entities available to add to the to_redact dict.

        :param:
        to_redact: dict

        :return:
        choices: list
            A list of entities that haven't been added to the to_redact dict yet.
        """

        # If to_redact has keys, only show ents that have not already been chosen for redaction.
        if len(redact) > 0:
            choices = list(set(ents).difference(redact))
        else:
            choices = list(set(ents))

        return choices, redact

    def search_style(search_choice, redact):
        """Call browse all or browse label search to choose more entities for redaction."""

        possible_ents = ents_available(redact)[0]
        if search_choice == "By label":
            browse_by_label(possible_ents, redact)  # Use seen_labels from ent_labels
        elif search_choice == "Browse all":
            browse_all(possible_ents, redact)  # Use ents from ent_labels

    def ask_me(redact):
        """Add flag to show entity in pdf context before final pdf redaction is performed."""

        msg = "Check the entity texts you would like to see in their pdf context before making your final decision to redact. \
              If you know you want to redact the text everywhere it appears, leave the box unchecked."
        title = "Check to see text in pdf"
        ask = g.multchoicebox(msg, title, [x.encode('utf-8') for x in redact.keys()])
        g.msgbox(ask, "Label Choices", ok_button="Continue")

        return ask

    def prep_outfile(redact):
        """Write the entities chosen for redaction to json file and add the entity label and ask_me flag."""

        count = count_ents(doc)
        ask = ask_me(redact)
        for ent, num in redact.items():
            redact[ent] = {}
            redact[ent]['count'] = count[ent]
            if ent in ask:
                redact[ent]['ask_me'] = True
            else:
                redact[ent]['ask_me'] = False
            for label, e in label_index.items():
                if ent in e:
                    redact[ent]['label'] = label

        # Write dict to json out
        with open('redactions.json', 'w') as outfile:
            json.dump(redact, outfile)

    def edit(redact):
        """Allow user to remove entities from the redaction list before it is finalized."""

        edits = g.multchoicebox(msg="Click the boxes for the entities you want to remove from the redaction list.",
                        title="Edit Redaction Choices", choices=[x.encode('utf-8') for x in redact.keys()])

        for e in edits:
            if e in redact:
                redact.pop(e, None)

        return redact

    def verify_redaction(redact):
        """Verify the final list of entities to be redacted.

        :param:
        to_redact: dict
            A dict passed in by the browse or by label redact function.

        :return:
        to_redact: dict
            Final redaction dictionary to be written to out file.
        """

        verify_choice = g.buttonbox("To verify your redaction choices and exit, click Verify. \n To remove or edit your choices, click Edit.",
                    "Check or Edit Redaction Choices.", choices=["Verify", "Edit"])
        if verify_choice == "Verify":
            # Show all to_redact keys
            edit_choice = g.buttonbox("You have chosen to redact: \n {0} \n To save your choices, click Save and Exit. Otherwise, click Edit to change your choices.".format(redact.keys()), "Verify Redaction",
                        choices=["Save and Exit", "Edit"])

            if edit_choice == "Save and Exit":
                prep_outfile(redact)

            elif edit_choice == "Edit":
                edit(redact)
                prep_outfile(redact)

        if verify_choice == "Edit":
            # Assuming that after the edits, the redaction is ready to be verified and finished.
            edit(redact)
            prep_outfile(redact)

    def browse_by_label(choices, redact):
        """Choose entities to redact based on the spacy ent.label_."""

        # # Browse by ent label
        # print(type(redact))
        # If there are ents remaining that aren't in the redaction dict, show labels for redaction.
        if len(choices) > 0:
            msg = "These are the entity labels we found in this document. Please choose the ones you want to browse."
            title = "Entity Labels"
            label_choice = g.multchoicebox(msg, title, labels)
            g.msgbox(label_choice, "Label Choices", ok_button="Continue")

            redact_all = g.ynbox("Do you want to redact all entities with this label? ",
                                 "Entity Redaction", ("Yes", "No"))
            if redact_all is True:
                l_choice = [e.text for e in doc.ents if e.label_ in label_choice]
                for ent in l_choice:
                    if ent not in redact:
                        redact[ent] = {}

                    else:
                        # Count total number of ent.texts during verify_redaction().
                        pass

                if len(ents_available(redact)) > 0:
                    l_choice = g.buttonbox(
                        "If you would like to choose more words to redact, click Continue, otherwise click Exit",
                        "Verification", choices=['Continue', 'Exit'])

                    if l_choice == "Continue":
                        continue_search = g.buttonbox("Search by entity label or browse all entities",
                                                      "Entity Redaction",
                                                      choices=['By label', 'Browse all'])
                        search_style(continue_search, redact)

                    elif l_choice == "Exit":
                        verify_redaction(redact)
                else:
                    g.msgbox("All entities have been placed in your redaction list.", "Verification", ok_button="OK")
                    verify_redaction(redact)

            if redact_all is False:

                msg = "Choose which values to redact: "
                title = "Entities by label"
                # Choices from ents_available, only show ents once even if present multiple times.
                l_choice = g.multchoicebox(msg, title, choices)
                for ent in l_choice:
                    if ent not in redact:
                        redact[ent] = {}
                    else:
                        # Count total number of ent.text during verify_redaction().
                        pass
                g.msgbox("You chose to redact: {}".format(l_choice), "To Redact", ok_button="Continue")

                if len(ents_available(redact)) > 0:
                    continue_choice = g.buttonbox(
                        "If you would like to choose more words to redact, click Continue, otherwise click Exit",
                        "Verification", choices=['Continue', 'Exit'])

                    if continue_choice == "Continue":
                        continue_search = g.buttonbox("Search by entity label or browse all entities",
                                                      "Entity Redaction",
                                                      choices=['By label', 'Browse all'])
                        search_style(continue_search, redact)

                    elif continue_choice == "Exit":  # Exit button doesn't seem to be working
                        verify_redaction(redact)
                else:
                    g.msgbox("All entities have been placed in your redaction list.", "Verification", ok_button="OK")
                    verify_redaction(redact)

        elif len(choices) == 0:
            g.msgbox("All entities have already been placed in your redaction list.", "Verification",
                     ok_button="OK")
            verify_redaction(redact)

    def browse_all(choices, redact):
        """Choose entities to redact from list of all entities."""

        # Choose specific ents
        msg = "Choose which values to redact: "
        title = "Entities"
        if len(choices) > 0:
            choice = g.multchoicebox(msg, title, choices)
            for c in choice:
                if c not in redact:
                    redact[c] = {}
            g.msgbox("You chose to redact: {}".format(choice), "To Redact", ok_button="Continue")

            # If there are still ents available, then ask if they want to redact more.
            if len(ents_available(redact)) > 0:
                continue_choice = g.buttonbox("If you would like to choose more words to redact, click Continue, otherwise click Exit",
                            "Verification", choices=['Continue', 'Exit'])

                if continue_choice == "Continue":
                    # Browse all or by label
                    continue_search = g.buttonbox("Choose entities to redact by label or browse all entities",
                                                  "Entity Redaction", choices=['By label', 'Browse all'])

                    search_style(continue_search, redact)

                if continue_choice == "Exit":
                    # Verify to_redact
                    verify_redaction(redact)

            else:
                g.msgbox("All entities have already been placed in your redaction list.", "Verification",
                         ok_button="OK")
                verify_redaction(redact)

        else:  # If all ents have already been chosen for redaction
            if len(choices) == 0:
                g.msgbox("All entities have already been placed in your redaction list.", "Verification",
                         ok_button="OK")
                verify_redaction(redact)

    # Check if dir and collect all ents.
    # User must input path to directory, file name only not supported.
    if os.path.isdir(path):
        seen_labels = []
        ents = []
        label_list = []
        label_index = {}
        to_redact = {}
        for root, dirs, files in os.walk(path):
            for file in files:
                if re.search(r'.pdf', file):
                    text = textract.process(os.path.join(root, file))
                    text = text.decode('utf-8', 'ignore')
                    nlp = spacy.load('en_core_web_sm')
                    doc = nlp(text)

                    labels = ent_labels(doc)[0]
                    entities = ent_labels(doc)[1]
                    seen_labels.extend(labels)
                    ents.extend(entities)
                    label_list.extend(ent_labels(doc)[2])

        # Prep for how easygui will cast text strings.
        ents = [re.sub(r'\n{1,}', ' ', str(x.encode('utf-8'))) for x in ents]
        label_list = [(str(tup[0].encode('utf-8')), str(tup[1].encode('utf-8'))) for tup in label_list]
        # Make a dictionary of labels to ent.texts as strings.
        for tup in label_list:
            if tup[0] not in label_index:
                label_index[tup[0]] = [re.sub(r'\n{1,}', ' ', tup[1])]
            else:
                label_index[tup[0]].append(re.sub(r'\n{1,}', ' ', tup[1]))

        search = g.buttonbox("Choose entities to redact by label or browse all entities", "Entity Redaction",
                             choices=['By label', 'Browse all'])
        # Start redaction choosing.
        search_style(search, to_redact)



if __name__ == '__main__':
    main(sys.argv[1])

