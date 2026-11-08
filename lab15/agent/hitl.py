# Human-in-the-loop validation module
import datetime

class HITLManager:
    def __init__(self):
        self.audit_log = []

    def classify_risk(self, operation, entity_type, attributes):
        if operation == "DELETE":
            return "HIGH"
        if entity_type == "Substation" and "voltage" in attributes and attributes["voltage"] == 750:
            return "MEDIUM"
        if entity_type == "RelaySetting" and "current_a" in attributes:
            return "MEDIUM"
        if entity_type == "Comment" or operation == "ALIAS_ADD":
            return "LOW"
        return "MEDIUM"

    def submit_proposal(self, user_id, operation, entity_type, attributes, justification):
        risk = self.classify_risk(operation, entity_type, attributes)
        timestamp = datetime.datetime.now().isoformat()
        proposal = {
            "id": f"PROP-{len(self.audit_log) + 1:03d}",
            "timestamp": timestamp,
            "user_id": user_id,
            "operation": operation,
            "entity": entity_type,
            "attributes": attributes,
            "justification": justification,
            "risk_level": risk,
            "status": "APPROVED" if risk == "LOW" else "PENDING_APPROVAL"
        }
        self.audit_log.append(proposal)
        return proposal

    def review_proposal(self, prop_id, reviewer_id, decision, signature=None):
        for p in self.audit_log:
            if p["id"] == prop_id:
                if p["risk_level"] == "HIGH" and decision == "APPROVE":
                    p["status"] = "REJECTED_HIGH_RISK_POLICY"
                    p["reviewer"] = reviewer_id
                    return p
                p["status"] = "APPROVED_BY_HUMAN" if decision == "APPROVE" else "REJECTED_BY_HUMAN"
                p["reviewer"] = reviewer_id
                p["signature"] = signature
                return p
        return None