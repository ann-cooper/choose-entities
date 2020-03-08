import json

import easygui as g


class Redaction:
    """Assemble and output json file of all entities to redact.

    Attributes
    ----------
    redact: dict
        Object containing the entities marked for redaction,
        count of how many times the entity appears in the directory,
        and whether the user has added the ask_me flag.
    count: Counter
        A Counter of the occurrences of the entity in the directory.
    label_index: dict
        A dictionary with entity labels as keys and lists of entities as values.
    inverse_index: dict
        A dictionary with entities as keys and labels as values

    Methods
    -------
    ask_me()
        Add flag to show entity in pdf context before final pdf redaction is performed.
    prep_outfile(edits)
        Write the entities chosen for redaction to json file and add the entity label and ask_me flag.
    edit()
        Allow user to remove entities from the redaction list before it is finalized.
    verify_redaction()
        Verify the final list of entities to be redacted and allow user to either edit the redaction or output the file.
    """

    def __init__(self, redact, count, label_index):
        self.redact = {k.strip(): v for k, v in redact.items()}
        self.count = count
        self.label_index = label_index
        self.inverse_index = {i.strip(): k for k, v in label_index.items() for i in v}

    def ask_me(self):
        """Add flag to show entity in pdf context before final pdf redaction is performed."""

        msg = "Check the entity texts you would like to see in their pdf context before making your final decision to redact. \
            If you know you want to redact the text everywhere it appears, leave the box unchecked."
        title = "Check to see text in pdf"
        ask = g.multchoicebox(msg, title, [x for x in self.redact.keys()])
        g.msgbox(ask, "Label Choices", ok_button="Continue")

        return ask

    def prep_outfile(self, edits=[]):
        """Write the entities chosen for redaction to json file and add the entity label and ask_me flag."""

        # Update entity count and label
        self.redact = {
            ent: {"count": self.count[ent], "label": self.inverse_index[ent]}
            for ent in self.redact
            if ent not in edits
        }
        # Update ask_me value
        ask = self.ask_me()
        {self.redact[d].update({"a": True}) for d in self.redact if d in ask}
        # Write dict to json out
        with open("redactions.json", "w") as outfile:
            json.dump(self.redact, outfile)

    def edit(self):
        """Allow user to remove entities from the redaction list before it is finalized."""

        edits = g.multchoicebox(
            msg="Click the boxes for the entities you want to remove from the redaction list.",
            title="Edit Redaction Choices",
            choices=self.redact.keys(),
        )
        return edits

    def verify_redaction(self):
        """Verify the final list of entities to be redacted and allow user to either edit the redaction or output the file."""

        verify_choice = g.buttonbox(
            "To verify your redaction choices and exit, click Verify. \n To remove or edit your choices, click Edit.",
            "Check or Edit Redaction Choices.",
            choices=["Verify", "Edit"],
        )
        if verify_choice == "Verify":
            # Show all to_redact keys
            edit_choice = g.buttonbox(
                f"Redacting: {list(self.redact.keys())}",
                "Verify Redaction",
                choices=["Save and Exit", "Edit"],
            )

            if edit_choice == "Save and Exit":
                self.prep_outfile()

            elif edit_choice == "Edit":
                self.prep_outfile(edits=self.edit())

        if verify_choice == "Edit":
            self.prep_outfile(edits=self.edit())
