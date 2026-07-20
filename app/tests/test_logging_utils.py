from app.logging_utils import get_logger, log_event


def test_logging_helpers_import_and_emit():
    logger = get_logger("test.logger")
    assert logger.name == "test.logger"

    message = log_event(logger, "hello", status="ok")
    assert message["event"] == "hello"
    assert message["status"] == "ok"
