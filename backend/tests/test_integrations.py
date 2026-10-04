def test_integration_modules_import():

    from app.integrations.omnidocs import OmniDocsIntegration
    from app.integrations.karza import KarzaIntegration
    from app.integrations.iib import IIBIntegration

    assert OmniDocsIntegration is not None
    assert KarzaIntegration is not None
    assert IIBIntegration is not None