def number_to_text(number):
    """Given a number, convert it to text

    Args:
        number : The number to be converted

    Returns:
        text : the text after conversion  

    """
    number = str(number)
    if number[0] in '0123456789':
        return 'english'
    elif number[0] == '០១២៣៤៥៦៧៨៩':
        return 'khmer'
    else:
        return ''
    
    
    
