# parsers.py

import re

"""
This file holds all our parser classes.
"""

# --- HDFCParser Class ---
class HDFCParser:
    def __init__(self, pdf_text):
        self.text = pdf_text
    
    def get_last_4_digits(self):
        pattern = r"Card No:\s*\d{4}\s+\d{2}XX\s+XXXX\s+(\d{4})"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_due_date(self):
        pattern = r"Payment Due Date\s+Total Dues\s+Minimum Amount Due[\s\S]*?(\d{2}/\d{2}/\d{4})\s+"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_total_balance(self):
        pattern = r"Payment Due Date\s+Total Dues\s+Minimum Amount Due[\s\S]*?\d{2}/\d{2}/\d{4}\s+([\d,]+\.\d{2})"
        match = re.search(pattern, self.text)
        return match.group(1).replace(",", "") if match else None

    def get_transactions(self):
        pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+([\d,]+\.\d{2})(\s+Cr)?", re.MULTILINE)
        transactions = []
        for match in pattern.findall(self.text):
            if "Transaction Description" in match[1] or "NIKHIL KHANDELWAL" in match[1]:
                continue
            transactions.append({"date": match[0], "description": match[1].strip(), "amount": match[2].replace(",", ""), "type": "Credit" if match[3] else "Debit"})
        return transactions

# --- IDFCParser Class ---
class IDFCParser:
    def __init__(self, pdf_text):
        self.text = pdf_text

    def get_last_4_digits(self):
        pattern = r"Card Number:\s*XXXX\s+(\d{4})"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_due_date(self):
        pattern = r"Payment Due Date\s*(\d{2}/\d{2}/\d{4})"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_total_balance(self):
        pattern = r"Total Amount Due\s*r([\d,]+\.\d{2})"
        match = re.search(pattern, self.text)
        return match.group(1).replace(",", "") if match else None

    def get_transactions(self):
        pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.\d{2})(\s+CR)?", re.MULTILINE)
        transactions = []
        for match in pattern.findall(self.text):
            if "Transactional Details" in match[1]:
                continue
            transactions.append({"date": match[0], "description": match[1].strip(), "amount": match[2].replace(",", ""), "type": "Credit" if match[3] else "Debit"})
        return transactions

# --- AxisParser Class ---
class AxisParser:
    def __init__(self, pdf_text):
        self.text = pdf_text

    def get_last_4_digits(self):
        pattern = r"Credit Card Number\s+Credit Limit[\s\S]*?\d{6}\*{6}(\d{4})"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_due_date(self):
        pattern = r"Payment Due Date\s+Statement Generation Date\s*[\s\S]*?\d{2}/\d{2}/\d{4}\s+-\s+\d{2}/\d{2}/\d{4}\s+(\d{2}/\d{2}/\d{4})"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_total_balance(self):
        pattern = r"Total Payment Due\s+Minimum Payment Due[\s\S]*?([\d,]+\.\d{2})\s+Dr"
        match = re.search(pattern, self.text)
        return match.group(1).replace(",", "") if match else None

    def get_transactions(self):
        pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.\d{2})\s+(Dr|Cr)", re.MULTILINE)
        transactions = []
        for match in pattern.findall(self.text):
            if "TRANSACTION DETAILS" in match[1]:
                continue
            transactions.append({"date": match[0], "description": match[1].strip(), "amount": match[2].replace(",", ""), "type": "Credit" if match[3] == "Cr" else "Debit"})
        return transactions

# --- ICICIParser Class ---
class ICICIParser:
    def __init__(self, pdf_text):
        self.text = pdf_text

    def get_last_4_digits(self):
        pattern = r"Card Number : \d{4}\s+XXXX\s+XXXX\s+(\d{3,4})"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_due_date(self):
        pattern = r"Due Date : (\d{2}/\d{2}/\d{4})"
        match = re.search(pattern, self.text)
        return match.group(1) if match else None

    def get_total_balance(self):
        pattern = r"Your Total Amount Due[\s\S]*?\|\s*([\d,]+\.\d{2})"
        match = re.search(pattern, self.text)
        return match.group(1).replace(",", "") if match else None

    def get_transactions(self):
        pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.\d{2})(\s+CR)?$", re.MULTILANE)
        transactions = []
        for match in pattern.findall(self.text):
            if ("Amortization" in match[1] or "CGST" in match[1] or "SGST" in match[1] or "FLIPKART PAYMENTS" in match[1]):
                continue
            transactions.append({"date": match[0], "description": match[1].strip(), "amount": match[2].replace(",", ""), "type": "Credit" if match[3] else "Debit"})
        return transactions