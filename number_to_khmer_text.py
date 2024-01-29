def number_to_khmer_text(number):
    """Given a number, convert it to text

    Args:
        number : The number to be converted

    Returns:
        text : the text after conversion  

    """
    number = kh_num_to_num(number)
    number = numtokhtext(number)
    return number
    
def numtokhtext(number):
    
    khmer_units = ['មួយ', 'ពីរ', 'បី', 'បួន', 'ប្រាំ', 'ប្រាំមួយ', 'ប្រាំពីរ', 'ប្រាំបី', 'ប្រាំបួន']
    khmer_tens = ['ដប់', 'ម្ភៃ', 'សាមសិប', 'សែសិប', 'ហាសិប', 'ហុកសិប', 'ចិតសិប', 'ប៉ែតសិប', 'កៅសិប']
    khmer_hundreds = ['មួយរយ', 'ពីររយ', 'បីរយ', 'បួនរយ', 'ប្រាំរយ', 'ប្រាំមួយរយ', 'ប្រាំពីររយ', 'ប្រាំបីរយ', 'ប្រាំបួនរយ']
    khmer_thousands = ['មួយពាន់', 'ពីរពាន់', 'បីពាន់', 'បួនពាន់', 'ប្រាំពាន់', 'ប្រាំមួយពាន់', 'ប្រាំពីរពាន់', 'ប្រាំបីពាន់', 'ប្រាំបួនពាន់']
    khmer_ten_thousands = ['មួយម៉ឺន', 'ពីរម៉ឺន', 'បីម៉ឺន', 'បួនម៉ឺន', 'ប្រាំម៉ឺន', 'ប្រាំមួយម៉ឺន', 'ប្រាំពីរម៉ឺន', 'ប្រាំបីម៉ឺន', 'ប្រាំបួនម៉ឺន']
    khmer_hundred_thousands = ['មួយសែន', 'ពីរសែន', 'បីសែន', 'បួនសែន', 'ប្រាំសែន', 'ប្រាំមួយសែន', 'ប្រាំពីរសែន', 'ប្រាំបីសែន', 'ប្រាំបួនសែន']
    khmer_millions = ['មួយលាន', 'ពីរលាន', 'បីលាន', 'បួនលាន', 'ប្រាំលាន', 'ប្រាំមួយលាន', 'ប្រាំពីរលាន', 'ប្រាំបីលាន', 'ប្រាំបួនលាន']
    text = ''
    length = len(str(number))
    if length <= 9:
        while number > 0:
            if number >= 100000000:
                text += khmer_hundreds[int(number // 100000000) - 1]
                number = number % 100000000
                if number < 1000000:
                    text += 'លាន'
            elif number >= 10000000:
                text += khmer_tens[int(number // 10000000) - 1]
                number = number % 10000000
                if number < 1000000:
                    text += 'លាន'
            elif number >= 1000000:
                text += khmer_millions[int(number // 1000000) - 1]
                number = number % 1000000
            elif number >= 100000:
                text += khmer_hundred_thousands[int(number // 100000) - 1]
                number = number % 100000
            elif number >= 10000:
                text += khmer_ten_thousands[int(number // 10000) - 1]
                number = number % 10000
            elif number >= 1000:
                text += khmer_thousands[int(number // 1000) - 1]
                number = number % 1000
            elif number >= 100:
                text += khmer_hundreds[int(number // 100) - 1]
                number = number % 100
            elif number >= 10:
                text += khmer_tens[int(number // 10) - 1]
                number = number % 10
            elif number >= 1:
                text += khmer_units[int(number) - 1]
                number = number % 1
            elif number == 0:
                text += 'សូន្យ'
                break
            else:
                text += ''
                break
    else:
        text += ''

    return text

def kh_num_to_num(number):
    number = str(number)
    khmer_units = ['០', '១', '២', '៣', '៤', '៥', '៦', '៧', '៨', '៩']
    number_units = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    new_number = ''
    for num in number:
        if num in khmer_units:
            new_number += number_units[khmer_units.index(num)]
        elif num in number_units:
            new_number += num
        else:
            return ''
    return int(new_number)

    
print(kh_num_to_num('0១១33២២33១១'))