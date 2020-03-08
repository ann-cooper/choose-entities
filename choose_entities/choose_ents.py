import sys

import easygui as g

from prep_docs import LabelDocs
from redaction import Redaction


class SearchEnts:
    """Handles choosing entities to redact through browsing or by label.

    Attributes
    ----------
    ents: list
        Spacy entities.
    label_list: list
        Tuples of the entity and its label.
    label_index: dict
        Index of labels to list of entities with that label.
    inv_idx: dict
        Index of entity to label.
    count: Counter
        Count of instances of each entity.
    redact: dict
        Entities marked for redaction.

    Methods
    -------
    ents_available()
        Return list of entities that have not been marked for redaction.
    redact_by_label(label_choice, redact_all)
        Add all ents for certain label(s) to the redact dict.
    browse_ents_by_label(labels)
        Choose individual entities to redact from label(s).
    continue_choosing()
        Allow user to continue choosing entities to redact or to verify and exit.
    browse_by_label()
        Choose entities to redact based on the spacy ent.label_.

    """

    def __init__(self, ents=[], label_list=[], label_index={}, inv_idx={}, count={}):
        self.ents = ents
        self.label_list = label_list
        self.label_index = label_index
        self.inv_idx = inv_idx
        self.count = count
        self.redact = {}

    def ents_available(self):
        """Check if there are still entities available to add to the to_redact dict.

        Returns
        -------
        choices: list
            A list of entities that haven't been added to the to_redact dict yet.
        """
        # If to_redact has keys, only show ents that have not already been chosen for redaction.
        if len(self.redact) > 0:
            self.choices = list(set(self.ents).difference(self.redact))
        else:
            self.choices = list(set(self.ents))
        return self.choices

    def redact_by_label(self, label_choice, redact_all=False):
        """Add all ents to redact object by label.

        Parameters
        ----------
        label_choice: list
            Labels from browse_by_label.
        redact_all: bool
            Bool from browse_by_label.

        Returns
        -------
        redact: dict
            Updated redact dict.
        """

        if redact_all is True:
            applicable_ents = [
                x
                for sublist in [self.label_index[label] for label in label_choice]
                for x in sublist
            ]
            # Add entities to redact dict.
            for ent in applicable_ents:
                if ent not in self.redact:
                    self.redact[ent] = {}
                else:
                    # Count total number of ent.texts during verify_redaction().
                    pass
            return self.redact

    def browse_ents_by_label(self, labels):
        """Choose individual entities to redact from label(s).

        Parameters
        ----------
        labels: list
            Labels chosen in browse_by_label.

        Returns
        -------
        redact: dict
            Updated redact dict.
        """
        msg = "Choose which values to redact: "
        title = "Entities by label"
        available_ents = self.ents_available()
        choices = [ent for ent in available_ents if self.inv_idx[ent] in labels]
        # Choices from ents_available, only show ents once even if present multiple times.
        l_choice = g.multchoicebox(msg, title, choices)
        for ent in l_choice:
            if ent not in self.redact:
                self.redact[ent] = {}
            else:
                # Count total number of ent.text during verify_redaction().
                pass
        g.msgbox(
            "You chose to redact: {}".format(l_choice),
            "To Redact",
            ok_button="Continue",
        )
        return self.redact

    def continue_choosing(self):
        """Allow user to continue choosing entities to redact or to verify and exit."""

        l_choice = g.buttonbox(
            "If you would like to choose more words to redact, click Continue, otherwise click Exit",
            "Verification",
            choices=["Continue", "Exit"],
        )

        if l_choice == "Continue":
            continue_search = g.buttonbox(
                "Search by entity label or browse all entities",
                "Entity Redaction",
                choices=["By label", "Browse all"],
            )
            self.search_style(continue_search)

        elif l_choice == "Exit":
            Redaction(self.redact, self.count, self.label_index).verify_redaction()

    def browse_by_label(self):
        """Choose entities to redact based on the spacy ent.label_."""

        choices = self.ents_available()
        # If there are ents remaining that aren't in the redaction dict, show labels for redaction.
        if len(choices) > 0:
            msg = "These are the entity labels we found in this document. Please choose the ones you want to browse."
            title = "Entity Labels"
            # Labels is the available labels that have un-redacted ents.
            labels = list(self.label_index.keys())
            label_choice = g.multchoicebox(msg, title, labels)
            g.msgbox(label_choice, "Label Choices", ok_button="Continue")

            redact_all = g.ynbox(
                "Do you want to redact all entities with this label? ",
                "Entity Redaction",
                ("Yes", "No"),
            )
            if redact_all is True:
                self.redact = self.redact_by_label(label_choice, redact_all=True)

                if len(choices) > 0:
                    self.continue_choosing()
                else:
                    g.msgbox(
                        "All entities have been placed in your redaction list.",
                        "Verification",
                        ok_button="OK",
                    )
                    Redaction(
                        self.redact, self.count, self.label_index
                    ).verify_redaction()

            elif redact_all is False:
                # Allow user to choose specific entities from that label and add to the redact dict.
                self.redact = self.browse_ents_by_label(label_choice)
                if len(choices) > 0:
                    self.continue_choosing()
                else:
                    g.msgbox(
                        "All entities have been placed in your redaction list.",
                        "Verification",
                        ok_button="OK",
                    )
                    Redaction(
                        self.redact, self.count, self.label_index
                    ).verify_redaction()

        elif len(choices) == 0:
            g.msgbox(
                "All entities have already been placed in your redaction list.",
                "Verification",
                ok_button="OK",
            )
            Redaction(self.redact, self.count, self.label_index).verify_redaction()

    def browse_all(self):
        """Choose entities to redact from list of all entities."""

        msg = "Choose which values to redact: "
        title = "Entities"
        choices = self.ents_available()
        if len(choices) > 0:
            choice = g.multchoicebox(msg, title, choices)
            for c in choice:
                if c not in self.redact:
                    self.redact[c] = {}
            g.msgbox(
                "You chose to redact: {}".format(choice),
                "To Redact",
                ok_button="Continue",
            )

            # If there are still ents available, ask if they want to redact more.
            if len(self.ents_available()) > 0:
                continue_choice = g.buttonbox(
                    "If you would like to choose more words to redact, click Continue, otherwise click Exit",
                    "Verification",
                    choices=["Continue", "Exit"],
                )

                if continue_choice == "Continue":
                    continue_search = g.buttonbox(
                        "Choose entities to redact by label or browse all entities",
                        "Entity Redaction",
                        choices=["By label", "Browse all"],
                    )

                    self.search_style(continue_search)

                if continue_choice == "Exit":
                    Redaction(
                        self.redact, self.count, self.label_index
                    ).verify_redaction()

            else:
                g.msgbox(
                    "All entities have already been placed in your redaction list.",
                    "Verification",
                    ok_button="OK",
                )
                Redaction(self.redact, self.count, self.label_index).verify_redaction()
        # If all ents have already been chosen for redaction
        else:
            if len(choices) == 0:
                g.msgbox(
                    "All entities have already been placed in your redaction list.",
                    "Verification",
                    ok_button="OK",
                )
                Redaction(self.redact, self.count, self.label_index).verify_redaction()

    def search_style(self, search_choice):
        """Call browse all or browse label search to choose more entities for redaction.

        Parameters
        ----------
        search_choice: str
            User chooses either 'by label' or 'browse all'.
        """

        if search_choice == "By label":
            self.browse_by_label()
        elif search_choice == "Browse all":
            self.browse_all()

    def start_search(self):
        self.search = g.buttonbox(
            "Choose entities to redact by label or browse all entities",
            "Entity Redaction",
            choices=["By label", "Browse all"],
        )

        self.search_style(self.search)


if __name__ == "__main__":
    labeled_text = LabelDocs(sys.argv[1])
    SearchEnts(
        ents=labeled_text.ents,
        label_list=labeled_text.label_list,
        label_index=labeled_text.index,
        inv_idx=labeled_text.inv_idx,
        count=labeled_text.count,
    ).start_search()
