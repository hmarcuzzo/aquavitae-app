import contextlib

from sqlalchemy import event


@contextlib.contextmanager
def force_nested_transaction_forever(session, commit_on_complete=True):
    """
    Keep re-entering a nested transaction everytime a transaction ends.
    """
    d = {"nested": session.begin_nested()}

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        # Start another nested trans if the prior one is no longer active.
        if not d["nested"].is_active:
            d["nested"] = session.begin_nested()

    try:
        yield
    finally:
        # Stop trapping us in perpetual nested transactions.
        # Is this the right place for this ?
        event.remove(session, "after_transaction_end", end_savepoint)

    # This seems like it would be error-prone.
    if commit_on_complete and d["nested"].is_active:
        d.pop("nested").commit()
