"""
Fundamentos da Programação - Projeto 1

Francisco Salgueiro nº103345
2/11/2021
fgcdbs@gmail.com
"""

###################################################

# 1. CORREÇÃO DO DOCUMENTO

###################################################


def corrigir_palavra(palavra):
    """
    Retorna cad. carateres sem letras maiúsculas e minúsculas alternadas

    corrigir_palavra: cad. carateres-> cad. carateres
    """

    # palavras de uma letra não são corrigidas
    if len(palavra) <= 1:
        return palavra

    # se há erro nos dois primeiros carateres, ignora-os
    if palavra[0].lower() == palavra[1].lower() and palavra[0] != palavra[1]:
        return corrigir_palavra(palavra[2:])

    else:
        palavra_out = palavra[0] + corrigir_palavra(palavra[1:])
        if palavra == palavra_out:  # caso já não haja mais nada a eliminar
            return palavra_out
        return corrigir_palavra(palavra_out)


def eh_anagrama(pal1, pal2):
    """
    Retorna True se os argumentos forem anagramas e False se não forem

    eh_anagrama: cad. carateres x cad. carateres -> booleano
    """

    if sorted(pal1.lower()) == sorted(pal2.lower()):
        return True
    return False


def corrigir_doc(doc):
    """
    Retorna cad. de carateres de entrada com palavras corrigidas sem anagramas

    corrigir_doc: cad. carateres -> cad. carateres
    """

    # verificação do argumento
    if (
        not isinstance(doc, str)
        or not doc.replace(" ", "").isalpha()
        or "  " in doc
    ):
        raise ValueError("corrigir_doc: argumento invalido")

    doc = corrigir_palavra(doc)
    palavras = doc.split()

    # elimina todos os anagramas diferentes de si próprios
    while True:
        for i in range(len(palavras) - 1):
            for j in range(i + 1, len(palavras)):
                if (
                    eh_anagrama(palavras[i], palavras[j])
                    and palavras[i].lower() != palavras[j].lower()
                ):
                    del palavras[j]
                    break
            else:
                continue
            break
        else:
            break

    doc = " ".join(palavras)
    return doc


###################################################

# 2. DESCOBERTA DO PIN

###################################################


def obter_posicao(char, pos):
    """
    Retorna o inteiro que corresponde à nova posição após o movimento

    obter_posicao: cad. carateres × inteiro -> inteiro
    """

    if char == "C" and pos > 3:
        pos -= 3
    if char == "B" and pos < 7:
        pos += 3
    if char == "E" and (pos-1) % 3 > 0:
        pos -= 1
    if char == "D" and (pos-1) % 3 < 2:
        pos += 1
    return pos


def obter_digito(chars, pos):
    """
    Devolve inteiro correspondente ao dígito a marcar após todos os movimentos

    obter_digito: cad. carateres × inteiro -> inteiro
    """

    for char in chars:
        pos = obter_posicao(char, pos)
    return pos


def obter_pin(tuplo):
    """
    Retorna tuplo de inteiros com pin codificado com tuplo de movimentos

    obter_pin: tuplo -> tuplo
    """

    # verificação do argumento
    if not isinstance(tuplo, tuple) or not 4 <= len(tuplo) <= 10:
        raise ValueError("obter_pin: argumento invalido")

    pos = 5
    pin = ()
    for seq in tuplo:
        # verificação de cada elemento do tuplo
        if (
            not isinstance(seq, str)
            or len(seq) == 0
            or not all(c in "CBED" for c in seq)
        ):
            raise ValueError("obter_pin: argumento invalido")

        pos = obter_digito(seq, pos)
        pin = pin + (pos,)
    return pin


###################################################

# 3. VERIFICAÇÃO DE DADOS

###################################################


def eh_entrada(entrada):
    """
    Retorna True sse o seu argumento corresponde a uma entrada da BDB

    eh_entrada: universal -> booleano
    """

    if not isinstance(entrada, tuple) or len(entrada) != 3:
        return False

    cifra = entrada[0]
    checksum = entrada[1]
    codigo = entrada[2]

    if (
        not isinstance(cifra, str)
        or not isinstance(checksum, str)
        or not isinstance(codigo, tuple)
        or not cifra.replace("-", "").isalpha()  # cifra só tem letras e hífens
        or "--" in cifra
        or cifra[0] == "-"
        or cifra[-1] == "-"
        or not cifra.islower()
        or checksum[0] != "["
        or checksum[-1] != "]"
        or len(checksum) != 7
        or not checksum[1:-1].isalpha()
        or not checksum.islower()
        or len(codigo) < 2
        or not all(isinstance(v, int) and v >= 0 for v in codigo)
    ):
        return False

    return True


def validar_cifra(cifra, checksum):
    """
    Retorna True sse a sequência de controlo é coerente com a cifra

    validar_cifra: cad. carateres × cad. carateres -> booleano
    """

    # transforma cifra em cad. carateres por ordem alfabética
    cifra = cifra.replace("-", "")
    cifra = "".join(sorted(cifra))

    # contador de frequências de cada letra
    freq = {}
    for char in cifra:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    freq = tuple((sorted(freq, key=freq.get, reverse=True)))
    # reverte-se freq pq o sorted ordena por ordem crescente por defeito

    checksum = checksum[1:-1]  # elimina os parênteses retos
    if not all(checksum[i] == freq[i] for i in range(5)):
        return False

    return True


def filtrar_bdb(lista):
    """
    Retorna lista de entradas com checksum incoerente com a cifra

    filtrar_bdb: lista -> lista
    """

    # verificação do argumento
    if not isinstance(lista, list) or len(lista) < 1:
        raise ValueError("filtrar_bdb: argumento invalido")

    incoerente = []
    for entrada in lista:
        # verificação de cada entrada na lista
        if not eh_entrada(entrada):
            raise ValueError("filtrar_bdb: argumento invalido")

        if not validar_cifra(entrada[0], entrada[1]):
            incoerente.append(entrada)
    return incoerente


###################################################

# 4. DESENCRIPTAÇÃO DE DADOS

###################################################


def obter_num_seguranca(codigo):
    """
    Retorna a menor diferença positiva entre qualquer par de números

    obter_num_seguranca: tuplo -> inteiro
    """

    comprimento = len(codigo)
    dif = float("inf")

    # para cada par de números, se a diferença for menor que dif, substitui dif
    for i in range(comprimento - 1):
        for j in range(i + 1, comprimento):
            if abs(codigo[i] - codigo[j]) < dif:
                dif = abs(codigo[i] - codigo[j])
    return dif


def decifrar_texto(cifra, codigo):
    """
    Retorna o texto decifrado de acordo com o número de segurança

    decifrar_texto: cad. carateres × inteiro -> cad. carateres
    """

    descod = ""
    for i, letra in enumerate(cifra):
        if letra == "-":
            descod += " "
            continue

        if i % 2 == 0:
            extra = 1
        else:
            extra = -1

        # transforma o caratere num numero entre 0 e 25
        # adiciona o codigo e o extra, modulo 26
        # volta a transformar num caratere de a a z
        descod += chr((ord(letra) - 97 + codigo + extra) % 26 + 97)
    return descod


def decifrar_bdb(lista):
    """
    Retorna uma lista contendo o texto das entradas decifradas

    decifrar_bdb: lista -> lista
    """

    # verificação do argumento
    if not isinstance(lista, list) or len(lista) < 1:
        raise ValueError("decifrar_bdb: argumento invalido")

    decifrados = []
    for entrada in lista:
        # verificação de cada entrada na lista
        if not eh_entrada(entrada):
            raise ValueError("decifrar_bdb: argumento invalido")

        num_seguranca = obter_num_seguranca(entrada[2])
        texto = decifrar_texto(entrada[0], num_seguranca)
        decifrados.append(texto)
    return decifrados


###################################################

# 5. DEPURAÇÃO DE SENHAS

###################################################


def eh_utilizador(utilizador):
    """
    Retorna True sse o argumento é um dicionário com informação de utilizador

    eh_utilizador: universal -> booleano
    """

    if (
        not isinstance(utilizador, dict)
        or not all(c in utilizador for c in ("pass", "name", "rule"))
        or len(utilizador) != 3
    ):
        return False

    password = utilizador["pass"]
    name = utilizador["name"]
    rule = utilizador["rule"]

    if (
        not isinstance(password, str)
        or len(password) < 1
        or not isinstance(name, str)
        or len(name) < 1
        or not ("vals" in rule and "char" in rule)
        or not isinstance(rule, dict)
        or not isinstance(rule["vals"], tuple)
        or not isinstance(rule["char"], str)
        or len(rule) != 2
        or len(rule["vals"]) != 2
        or not all(isinstance(v, int) and v > 0 for v in rule["vals"])
        or rule["vals"][0] > rule["vals"][1]
        or not rule["char"].isalpha()
        or len(rule["char"]) != 1
        or not rule["char"].islower()
    ):
        return False
    return True


def eh_senha_valida(senha, regra):
    """
    Retorna True sse a senha cumpre as regras gerais e individual

    eh_senha_valida: cad. carateres × dicionário -> booleano
    """

    # REGRAS GERAIS
    vogais = 0
    consecutivo = False
    comprimento = len(senha)
    for i in range(comprimento):
        if i < comprimento - 1 and senha[i] == senha[i + 1]:
            consecutivo = True
        if senha[i] in "aeiou":
            vogais += 1
    if not (vogais > 2 and consecutivo):
        return False

    # REGRA INDIVIDUAL
    if not regra["vals"][0] <= senha.count(regra["char"]) <= regra["vals"][1]:
        return False
    return True


def filtrar_senhas(utilizadores):
    """
    Retorna lista de nomes dos utilizadores com senhas erradas

    filtrar senhas: lista -> lista
    """

    # verificação do argumento
    if not isinstance(utilizadores, list) or len(utilizadores) < 1:
        raise ValueError("filtrar_senhas: argumento invalido")

    erradas = []
    for user in utilizadores:
        # verificação de cada utilizador
        if not eh_utilizador(user):
            raise ValueError("filtrar_senhas: argumento invalido")

        if not eh_senha_valida(user["pass"], user["rule"]):
            erradas.append(user["name"])
    erradas = sorted(erradas)
    return erradas
