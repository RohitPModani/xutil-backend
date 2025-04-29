def to_base(n: int, base: int) -> str:
    if not 2 <= base <= 36:
        raise ValueError("Target base must be between 2 and 36")
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while n:
        result = digits[n % base] + result
        n //= base
    return result or "0"

def base_convert_logic(number: str, source_base: int, target_base: int) -> str:
    if source_base < 2 or source_base > 36:
        raise ValueError(f"Source base {source_base} is not supported")
    if target_base < 2 or target_base > 36:
        raise ValueError(f"Target base {target_base} is not supported")
    try:
        decimal = int(number, source_base)
        result = to_base(decimal, target_base)
        return result.upper()
    except ValueError as e:
        raise ValueError(f"Invalid conversion: {str(e)}")