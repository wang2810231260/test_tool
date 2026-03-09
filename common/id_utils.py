
import random
import sys
import os

# Add current directory to sys.path to ensure local imports work
sys.path.append(os.getcwd())

from common.logger import logger

class CBUUtil:
    
    @staticmethod
    def generate_cbu():
        """
        Generate a valid CBU string.
        """
        bank_code = [random.randint(0, 9) for _ in range(3)]
        digit_3 = random.randint(0, 9)
        branch_code = [random.randint(0, 9) for _ in range(3)]
        
        sum1 = (bank_code[0] * 7 + 
                bank_code[1] * 1 + 
                bank_code[2] * 3 + 
                digit_3 * 9 + 
                branch_code[0] * 7 + 
                branch_code[1] * 1 + 
                branch_code[2] * 3)
        
        digit_7 = (10 - sum1 % 10) % 10
        
        block1 = bank_code + [digit_3] + branch_code + [digit_7]
        account_prefix = [random.randint(0, 9) for _ in range(13)]
        
        weights = [3, 9, 7, 1]
        sum2 = 0
        for i in range(13):
            sum2 += account_prefix[i] * weights[i % 4]
            
        digit_21 = (10 - sum2 % 10) % 10
        
        block2 = account_prefix + [digit_21]
        
        cbu_list = block1 + block2
        cbu_str = "".join(map(str, cbu_list))
        return cbu_str
   


class CUITUtil:
    
    INDIVIDUAL_PREFIXES = ["20", "23", "24", "27"]
    COMPANY_PREFIXES = ["30", "33", "34"]
    INTERNATIONAL_PREFIXES = ["50", "51", "55"]
    ALL_VALID_PREFIXES = INDIVIDUAL_PREFIXES + COMPANY_PREFIXES + INTERNATIONAL_PREFIXES
    
    WEIGHTS = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    @staticmethod
    def generate_cuit(is_company=False):

        if is_company:
            prefix = random.choice(CUITUtil.COMPANY_PREFIXES)
        else:
            prefix = random.choice(CUITUtil.INDIVIDUAL_PREFIXES)
        dni = "".join([str(random.randint(0, 9)) for _ in range(8)])
        body = prefix + dni
        check_digit = CUITUtil.calculate_check_digit(body)
        cuit = body + check_digit
        return cuit

    @staticmethod
    def calculate_check_digit(ten_digit_string):
        """
        Calculates the check digit using weighted sum mod 11 algorithm.
        """
        total = 0
        for i in range(10):
            digit = int(ten_digit_string[i])
            total += digit * CUITUtil.WEIGHTS[i]
            
        remainder = total % 11
        difference = 11 - remainder
        
        if difference == 11:
            return '0'
        elif difference == 10:
            return '9'
        else:
            return str(difference)

