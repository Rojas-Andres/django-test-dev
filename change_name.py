import os
import sys


def update_name(path_name, line_new, line_to_replace):
    try:
        with open(path_name, "r") as f:
            content = f.read()
        new_content = content.replace(line_to_replace, line_new)
        with open(path_name, "w") as f:
            f.write(new_content)
        print(f"Se ha actualizado el puerto en {path_name} a {line_new}")
    except FileNotFoundError:
        print(f"Error: El archivo {path_name} no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <environment>")
        sys.exit(1)

    environment = sys.argv[1]
    print("environment", environment)
    supervisor_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "template.yml"
    )
    update_name(supervisor_path, f"BTI{environment}", "BTI")
