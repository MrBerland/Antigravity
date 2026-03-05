import sys
from unittest.mock import MagicMock

# Mock Google Cloud libraries to allow testing without installation
sys.modules['google'] = MagicMock()
sys.modules['google.cloud'] = MagicMock()
sys.modules['google.cloud.storage'] = MagicMock()
sys.modules['google.cloud.bigquery'] = MagicMock()
sys.modules['google.oauth2'] = MagicMock()
sys.modules['googleapiclient'] = MagicMock()
sys.modules['googleapiclient.discovery'] = MagicMock()

from main import should_ingest

# Mock Data Generator
def create_mock_email(sender, subject, snippet, labels=[]):
    return {
        'snippet': snippet,
        'labelIds': labels,
        'payload': {
            'headers': [
                {'name': 'From', 'value': sender},
                {'name': 'Subject', 'value': subject}
            ]
        }
    }

def run_tests():
    print("running Bouncer Security Tests...\n")
    
    # CASE 1: Explicit Label Block
    msg1 = create_mock_email('boss@augos.com', 'Q3 Strategy', 'Checking in', ['CONFIDENTIAL'])
    assert should_ingest(msg1) == False, "Failed: Should block CONFIDENTIAL label"
    print("✅ Passed: Blocked Confidential Label")

    # CASE 2: Keyword Block
    msg2 = create_mock_email('hr@augos.com', 'Payroll Updates', 'Please review')
    assert should_ingest(msg2) == False, "Failed: Should block 'Payroll' keyword"
    print("✅ Passed: Blocked Sensitive Keyword")

    # CASE 3: Internal Chatter (Block)
    msg3 = create_mock_email('tim@augos.com', 'Lunch?', 'Tacos?')
    assert should_ingest(msg3) == False, "Failed: Should block Internal Chatter"
    print("✅ Passed: Blocked Internal Chatter")

    # CASE 4: Internal Asset (Allow)
    msg4 = create_mock_email('tim@augos.com', 'Alert: Device MP-102', 'Sensor reading high')
    assert should_ingest(msg4) == True, "Failed: Should ALLOW Internal Asset mention"
    print("✅ Passed: Allowed Internal Asset (Device ID)")

    # CASE 5: External Email (Allow)
    msg5 = create_mock_email('client@external.com', 'New Project', 'Let us discuss')
    assert should_ingest(msg5) == True, "Failed: Should ALLOW External email"
    print("✅ Passed: Allowed External Email")

    print("\nALL TESTS PASSED.")

if __name__ == "__main__":
    run_tests()
