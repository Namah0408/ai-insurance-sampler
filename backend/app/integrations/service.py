import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.integrations.iib import IIBIntegration
from app.integrations.karza import KarzaIntegration
from app.integrations.omnidocs import OmniDocsIntegration


def run_all_integrations(
    proposal_id: uuid.UUID,
    db: Session,
) -> list[dict[str, Any]]:

    integrations = [
        OmniDocsIntegration(db),
        KarzaIntegration(db),
        IIBIntegration(db),
    ]

    results = []

    for integration in integrations:

        try:

            result = integration.check(proposal_id)

            results.append(
                {
                    "provider": integration.provider_name,
                    "status": "success",
                    "response": result,
                }
            )

        except Exception as error:

            results.append(
                {
                    "provider": integration.provider_name,
                    "status": "failed",
                    "response": {
                        "error": str(error),
                    },
                }
            )

    return results