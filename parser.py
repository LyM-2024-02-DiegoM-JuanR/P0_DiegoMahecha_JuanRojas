from lexer import tokenize, addVariable, addMacro, removeVariable, getMacrosDict

# Estado global del parser
tokens = []
pos = 0

# Funciones auxiliares para la gestión de tokens
def current_token():
    """Devuelve el token actual en el flujo de tokens."""
    if pos < len(tokens):
        return tokens[pos]
    return None

def consume():
    """Consume el token actual y avanza al siguiente."""
    global pos
    token = current_token()
    if token:
        pos += 1
    return token

def remaining_input():
    """Devuelve el texto restante de entrada desde la posición del token actual."""
    remaining_tokens = tokens[pos:]
    return ' '.join(token[1] for token in remaining_tokens)

# Función principal de análisis sintáctico
def parse(token_list):
    """Analiza toda la entrada, manejando bloques e instrucciones."""
    global tokens, pos
    
    tokens = token_list
    pos = 0
    
    while current_token():
        token = current_token()
        
        if token and token[0] == "EXEC":
            parse_exec_block()
            
        elif token and token[0] == "DEFINITION":
            parse_new_definition()

# Análisis de instrucciones individuales
def parse_instruction():
    token = current_token()
    
    if token and token[0] == "CONTROL_STRUCTURE":
        parse_control_structure()
        
    else:
        
        parse_command()

    assert current_token()[0] == "END", "Se esperaba ';' después de la instrucción" + tokens[pos-2][1] + tokens[pos-1][0] + tokens[pos][1] + tokens[pos+1][1] + tokens[pos+2][1]
    consume()  # Consume ';'

def parse_exec_block():
    token = consume()  # Consume la palabra clave EXEC
    assert token[0] == "EXEC", "Se esperaba 'EXEC'"
    parse_block()  # Analiza el bloque después de EXEC

def parse_command():
    token = current_token()
    
    if token[0] == "MACRO":
        
        parse_macro_call()
        return
        
    command = consume()  # Consume el comando
        
    if current_token()[0] == "ASSIGN":
        
        consume()  # Consume '='
        
        value_token = current_token()
        
        assert value_token[0] in ["NUMBER", "VARIABLE", "VALUE"], "Se esperaba un valor o variable después de '='"
        
        consume()  # Consume el valor


    if command[1] in ["turntomy", "turntothe", "walk", "jump", "drop", "pick", "grab", "letgo", "pop", "safeexe"]:
        assert current_token()[0] == "LPAREN", "Se esperaba '(' después del comando"
        consume()  # Consume '('

        param = current_token()

        if command[1] in ["turntomy", "turntothe"]:
            assert param[0] in ["DIRECTION", "ORIENTATION"], f"Se esperaba dirección u orientación para {command[1]}"
            consume()  # Consume el parámetro
        elif command[1] in ["walk", "jump", "drop", "pick", "grab", "letgo", "pop"]:
            assert param[0] in ["NUMBER", "VALUE", "VARIABLE"], f"Se esperaba un número para {command[1]}" 
            consume()  # Consume el parámetro
        elif command[1] == "safeexe":
            assert param[0] == "COMMAND", "Se esperaba un comando para safeExe"
            parse_command()

        assert current_token()[0] == "RPAREN", "Se esperaba ')' después del parámetro" 
        consume()  # Consume ')'

    elif command[1] == "moves":
        assert current_token()[0] == "LPAREN", "Se esperaba '(' después de moves"
        consume()  # Consume '('

        assert current_token()[0] == "DIRECTION", "Se esperaba una dirección" 
        directions = []
        while current_token()[0] == "DIRECTION":
            directions.append(current_token()[1])
            consume()  # Consume la dirección
            if current_token()[0] == "COMMA":
                consume()  # Consume ',' y espera la siguiente dirección
                assert current_token()[0] == "DIRECTION", "Se esperaba otra dirección después de ','"

        assert current_token()[0] == "RPAREN", "Se esperaba ')' después de la lista de direcciones"
        consume()  # Consume ')'
    
    if command[1] == "nop":
        pass  # nop no requiere procesamiento adicional
    
def parse_control_structure():
    token = consume()  # Consume la palabra clave de la estructura de control
    if token[1] == "if":
        parse_if()
    elif token[1] == "do":
        parse_do_while_loop()
    elif token[1] == "rep":
        parse_repeat_loop()

def parse_if():
    consume()  # Consume "("
    parse_conditional()  # Analiza la condición dentro del if
    consume()  # Consume ")"
    assert current_token()[0] == "CONTROL_STRUCTURE" and current_token()[1] == "then", "Se esperaba 'then'"
    consume()  # Consume 'then'
    parse_block()  # Analiza el bloque para la parte 'then'
    if current_token()[0] == "CONTROL_STRUCTURE" and current_token()[1] == "else":
        consume()  # Consume 'else'
        parse_block()  # Analiza el bloque para la parte 'else'
    assert current_token()[0] == "CONTROL_STRUCTURE" and current_token()[1] == "fi", "Se esperaba 'fi' para cerrar 'if'"
    consume()  # Consume 'fi'

def parse_do_while_loop():
    consume()  # Consume "("
    parse_conditional()  # Analiza la condición en el bucle do
    consume()  # Consume ")"
    parse_block()  # Analiza el bloque para el bucle do
    assert current_token()[0] == "CONTROL_STRUCTURE" and current_token()[1] == "od", "Se esperaba 'od' para cerrar 'do'"
    consume()  # Consume 'od'

def parse_repeat_loop():
    times_value = consume()  # Se espera un número para el número de repeticiones
    assert times_value[0] in ["NUMBER", "VALUE", "VARIABLE"] , "Se esperaba un número de repeticiones después de 'rep'"
    assert current_token()[0] == "CONTROL_STRUCTURE" and current_token()[1] == "times", "Se esperaba 'times' después del número"
    consume()  # Consume 'times'
    parse_block()  # Analiza el bloque del bucle
    assert current_token()[0] == "CONTROL_STRUCTURE" and current_token()[1] == "per", "Se esperaba 'per' para cerrar el bucle"
    consume()  # Consume 'per'

# Análisis de condicionales
def parse_conditional():
    token = current_token()
    if token[1] == "isblocked?":
        parse_isblocked()
    elif token[1] == "isfacing?":
        parse_isfacing()
    elif token[1] == "zero?":
        parse_zero()
    elif token[1] == "not":
        parse_not()
    else:
        error(f"Condicional inesperado: {token[1]}")

def parse_isblocked():
    consume()  # Consume 'isBlocked?'
    assert current_token()[0] == "LPAREN", "Se esperaba '(' después de isBlocked?"
    consume()  # Consume '('

    direction = current_token()
    assert direction[0] == "DIRECTION", "Se esperaba una dirección (left, right, front, back) para isBlocked?" 
    consume()  # Consume la dirección

    assert current_token()[0] == "RPAREN", "Se esperaba ')' después de la dirección en isBlocked?"
    consume()  # Consume ')'

def parse_isfacing():
    consume()  # Consume 'isFacing?'
    assert current_token()[0] == "LPAREN", "Se esperaba '(' después de isFacing?"
    consume()  # Consume '('

    orientation = current_token()
    assert orientation[0] == "ORIENTATION", "Se esperaba una orientación (north, south, east, west) para isFacing?"
    consume()  # Consume la orientación

    assert current_token()[0] == "RPAREN", "Se esperaba ')' después de la orientación en isFacing?"
    consume()  # Consume ')'

def parse_zero():
    consume()  # Consume 'zero?'
    assert current_token()[0] == "LPAREN", "Se esperaba '(' después de zero?"
    consume()  # Consume '('

    value = current_token()
    assert value[0] in ["NUMBER", "VALUE", "VARIABLE"], "Se esperaba un número para zero?"
    consume()  # Consume el número

    assert current_token()[0] == "RPAREN", "Se esperaba ')' después del número en zero?"
    consume()  # Consume ')'

def parse_not():
    consume()  # Consume 'not'
    assert current_token()[0] == "LPAREN", "Se esperaba '(' después de not"
    consume()  # Consume '('

    parse_conditional()

    assert current_token()[0] == "RPAREN", "Se esperaba ')' después de la condición en not"
    consume()  # Consume ')'

def parse_value():
    token = current_token()
    if token[0] == "VALUE":
        print(f"Valor reconocido: {token[1]}")
        consume()  # Consume el token de valor
    else:
        error(f"Valor inesperado: {token[1]}")

def parse_direction():
    token = current_token()
    if token[0] == "DIRECTION":
        print(f"Dirección reconocida: {token[1]}")
        consume()  # Consume el token de dirección
    else:
        error(f"Dirección inesperada: {token[1]}")

def parse_orientation():
    token = current_token()
    if token[0] == "ORIENTATION":
        print(f"Orientación reconocida: {token[1]}")
        consume()  # Consume el token de orientación
    else:
        error(f"Orientación inesperada: {token[1]}")

def parse_variable():
    token = current_token()
    if token[0] == "VARIABLE":
        print(f"Variable reconocida: {token[1]}")
        consume()  # Consume el token de variable
    else:
        error(f"Variable inesperada: {token[1]}")

def parse_macro_call():
    """Parsea la invocación de macros/funciones."""
    token = consume()
    macros = getMacrosDict()
    macro_name = token[1]

    assert current_token()[0] == "LPAREN", "Se esperaba '(' después del nombre del macro" 
    consume()  # Consume '('

    params = []
    while current_token()[0] != "RPAREN":
        param = consume()  # Parametro actual
        assert param[0] in ["NUMBER", "VARIABLE"], "Se esperaba un parámetro válido"

        params.append(param[1])

        if current_token()[0] == "COMMA":
            consume()  # Consume ',' entre los parámetros

    consume()  # Consume ')'

    expected_param_count = macros[macro_name]
    if len(params) != expected_param_count:
        error(f"El macro '{macro_name}' esperaba {expected_param_count} parámetros, pero recibió {len(params)}")


def parse_new_definition():
    token = consume()  # Consume la palabra clave NEW
    assert token[1] == "new", "Se esperaba 'new'"

    definition_type = consume()  # Se espera 'VAR' o 'MACRO'
    assert definition_type[1] in ["var", "macro"], "Se esperaba 'var' o 'macro'"

    if definition_type[1] == "var":
        parse_variable_definition()
    elif definition_type[1] == "macro":
        parse_macro_definition()

def parse_variable_definition():
    name_tokens = []
    while current_token()[0] != "ASSIGN":
        name_tokens.append(current_token()[1])
        consume()

    var_name = ''.join(name_tokens)

    consume()  # Consume '='

    value_token = consume()  # Se espera un valor para inicialización
    assert value_token[0] == "NUMBER", "Se esperaba un número para la inicialización de la variable"

    addVariable(var_name)

    re_tokenize_remaining_input()

def parse_macro_definition():
    """Parsea la definición de un macro (función) y registra su nombre y parámetros."""
    name_tokens = []

    # Recolectar tokens antes de '(' como el nombre del macro
    while current_token()[0] != "LPAREN":
        name_tokens.append(current_token()[1])
        consume()

    macro_name = ''.join(name_tokens)  # Concatenar los tokens para formar el nombre del macro

    consume()  # Consumir '('

    params = []

    # Recolectar los parámetros del macro
    while current_token()[0] != "RPAREN":
        param = consume()  # Nombre del parámetro
        assert param[0] == "GENERIC", "Se esperaba el nombre del parámetro"
        params.append(param[1])

        if current_token()[0] == "COMMA":
            consume()  # Consumir ',' entre parámetros

    consume()  # Consumir ')'

    # Registrar cada parámetro como variable local en el macro
    for param in params:
        addVariable(param)
        
    # Registrar el macro en el lexer junto con el número de parámetros
    addMacro(macro_name, len(params))

    # Retokenizar después de agregar los nuevos parámetros
    re_tokenize_remaining_input()

    # Asegurarse de que el bloque del macro esté definido dentro de llaves '{' '}' 
    assert current_token()[0] == "LBRACE", "Se esperaba '{' para iniciar el bloque del macro" 
    parse_block()  # Parsear el bloque del macro

    # Eliminar las variables temporales de los parámetros después de que el macro se haya definido
    for param in params:
        removeVariable(param)

    # Retokenizar después de eliminar los parámetros
    re_tokenize_remaining_input()

def re_tokenize_remaining_input():
    """Re-tokeniza la entrada restante después de definir una nueva variable o macro."""
    global tokens, pos
    remaining = remaining_input()
    new_tokens = tokenize(remaining)
    tokens = tokens[:pos] + new_tokens
    pos = len(tokens[:pos])

def parse_block():
    assert current_token()[0] == "LBRACE", "Se esperaba '{' para iniciar el bloque" + tokens[pos-2][1] + tokens[pos-1][1] + tokens[pos][1] + tokens[pos+1][1] + tokens[pos+2][1]
    consume()  # Consume '{'
    while current_token()[0] != "RBRACE":
        parse_instruction()  # Analiza las instrucciones dentro del bloque
    consume()  # Consume '}'

def error(message):
    raise SyntaxError(f"Error de sintaxis: {message}")

# Función principal
def main():
    # Lee el programa de entrada desde un archivo
    with open("pseudocode.txt", "r") as f:
        input_text = f.read()

    # Tokeniza la entrada usando el lexer
    token_list = tokenize(input_text)

    # Analiza la entrada y verifica la corrección sintáctica
    try:
        parse(token_list)
        print("El programa es sintácticamente correcto.")
    except AssertionError as e:
        print(f"Error de aserción: {e}")
    except SyntaxError as e:
        print(f"Error de sintaxis: {e}")

if __name__ == "__main__":
    main()
