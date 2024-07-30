import sqlite3

# Ele tenta se conectar com a tabela, e se ela não exitir ele vai criar
conn = sqlite3.connect('products.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS products
             (code TEXT, name TEXT, value REAL, category TEXT)''')   

def display_menu():   # Exibe o menu 
    print("""
█▀▄▀█ ▄▀█ █▀█ █▄▀ █▀▀ ▀█▀   █▀ █▄█ █▀ ▀█▀ █▀▀ █▀▄▀█
█░▀░█ █▀█ █▀▄ █░█ ██▄ ░█░   ▄█ ░█░ ▄█ ░█░ ██▄ █░▀░█""")

    print("""\n
        1 - Register Product
        2 - Remove Product 
        3 - Update Product
        4 - Display Products
        5 - Depreciation
        6 - Exit\n
        """)

def register_product(): # Registra o produto 
    new_code = input("\nDigite o Código serial do novo produto: ").upper()
    new_name = input("\nDigite o Nome do novo produto: ").upper()
    new_value = float(input("\nDigite o Valor do produto: "))
    new_category = input("\nDigite a Categoria do novo produto: ").upper()

    c.execute("SELECT * FROM products WHERE code=? OR name=?", (new_code, new_name))
    existing_product = c.fetchone()
    if existing_product:
        print("\nUm produto com este código ou nome já existe.")
        return

    c.execute("INSERT INTO products VALUES (?, ?, ?, ?)", (new_code, new_name, new_value, new_category))
    conn.commit()
    print(f'\nO produto foi adicionado com êxito!')
    
def remove_product(): # Remove um produto 
    c.execute("SELECT * FROM products")
    all_products = c.fetchall()
    if not all_products:
        print("\nNão há produtos para remover.")
        return
    
    print("\nProdutos disponíveis para remoção:")
    display_products()
    remove = int(input("\nDigite o número do produto que você deseja Remover: "))
    if remove < 0 or remove >= len(all_products):
        print("\nNúmero de produto inválido.")
        return

    removed_product = all_products.pop(remove)
    c.execute("DELETE FROM products WHERE code=?", (removed_product[0],))
    conn.commit()
    print("\nO produto foi removido com êxito!")

def update_product(): # Atualiza um produto 
    c.execute("SELECT * FROM products")
    all_products = c.fetchall()
    if not all_products:
        print("\nNão há produtos para atualizar.")
        return

    print("\nProdutos disponíveis para atualização:")
    display_products()
    update = int(input("\nDigite o número do produto que você deseja atualizar: "))
    if update < 0 or update >= len(all_products):
        print("\nNúmero de produto inválido.")
        return

    print("""\n
          1 - Código Serial
          2 - Nome
          3 - Valor
          4 - Categoria
          5 - Todas as Opções
          """)
    value_update = int(input("\nO que você gostaria de atualizar?  "))
    if value_update == 1:
        new_code = input("\nInsira o novo Código do produto: ")
        c.execute("UPDATE products SET code=? WHERE code=?", (new_code, all_products[update][0]))
    elif value_update == 2:
        new_name = input("Insira o novo Nome do produto: ")
        c.execute("UPDATE products SET name=? WHERE code=?", (new_name, all_products[update][0]))
    elif value_update == 3:
        new_value = float(input("Insira o novo Valor do produto: "))
        c.execute("UPDATE products SET value=? WHERE code=?", (new_value, all_products[update][0]))
    elif value_update == 4:
        new_category = input("Insira a nova Categoria do produto: ")
        c.execute("UPDATE products SET category=? WHERE code=?", (new_category, all_products[update][0]))
    elif value_update == 5:
        new_code = input("\nInsira o novo Código do produto: ")
        new_name = input("Insira o novo Nome do produto: ")
        new_value = float(input("Insira o novo Valor do produto: "))
        new_category = input("Insira a nova Categoria do produto: ")

        c.execute("UPDATE products SET code=?, name=?, value=?, category=? WHERE code=?", (new_code, new_name, new_value, new_category, all_products[update][0]))

    else: 
        print("\nValor inserido inválido")
    conn.commit()
    print("\nO produto foi Atualizado com êxito!")

def display_products(): # Exibe os produtos 
    c.execute("SELECT * FROM products")
    all_products = c.fetchall()
    if not all_products:
        print("\nNão há produtos para exibir.")
        return
    print("\nProdutos Adicionados: \n")
    for i, product in enumerate(all_products):
        print(f"{i}- Código: {product[0]}, Nome: {product[1]}, Valor: {product[2]}, Categoria: {product[3]}")

def depreciation(): # Faz a depreciação de um produto 
    depreciation_rate = 0.04
    print("\nA depreciação dada pelo sistema é de 4% no ano, e todos os produtos possuem 10 anos de duração")
    c.execute("SELECT * FROM products")
    all_products = c.fetchall()
    if not all_products:
        print("\nNão há produtos para ocorrer a depreciação.")
        return
    
    print("\nProdutos disponíveis para a depreciação:")
    display_products()
    number_depreciation = int(input("\nDigite o número do produto que você deseja depreciar: "))
    if number_depreciation < 0 or number_depreciation >= len(all_products):
        print("\nNúmero de produto inválido.")
        return
    
    year = int(input("Digite quantos anos o produto está parado no mercado: "))
    new_depreciation = all_products[number_depreciation][2] * depreciation_rate * year
    new_value = all_products[number_depreciation][2] - new_depreciation
    c.execute("UPDATE products SET value=? WHERE code=?", (new_value, all_products[number_depreciation][0]))
    conn.commit()
    print("\nDepreciação aplicada com sucesso!")

def start(): # Inicia o programa 
    while True:
        option = int(input("Digite qual opção você gostaria de seguir: "))
        if option == 1:
            register_product()
        elif option == 2:
            remove_product()
        elif option == 3:
            update_product()
        elif option == 4:
            display_products()
        elif option == 5:
            depreciation()
        elif option == 6:
            print("\nSaindo......")
            break
        else:
            print("\nNúmero não reconhecido")

display_menu()
start()
print("\nO Sistema fechou com êxito!")