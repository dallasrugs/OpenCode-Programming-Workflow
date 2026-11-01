def can_execute(state):
    # The caller saves drafts before submit.
    return not (state["busy"] or state["active"] or state["conflict"])
