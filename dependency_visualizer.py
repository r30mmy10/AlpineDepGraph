import subprocess
import argparse


def get_dependencies(package_name, max_depth, current_depth=1):
    if current_depth > max_depth:
        return []

    try:
        # Выполняем команду apk info для получения информации о зависимостях
        result = subprocess.run(['apk', 'info', '-R', package_name], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError:
        print(f"Ошибка при получении информации о пакете {package_name}")
        return []

    dependencies = []
    lines = output.splitlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith(package_name) and not line.startswith("depends on"):
            dependencies.append(line)

    all_dependencies = []
    for dep in dependencies:
        all_dependencies.append(dep)
        sub_deps = get_dependencies(dep, max_depth, current_depth + 1)
        all_dependencies.extend(sub_deps)

    return all_dependencies


def generate_mermaid(package_name, dependencies):
    mermaid_code = "graph TD\n"
    for dep in dependencies:
        mermaid_code += f"    {package_name} --> {dep}\n"
    return mermaid_code


def main():
    parser = argparse.ArgumentParser(description="Dependency graph visualizer for Alpine Linux packages.")
    parser.add_argument('--graph-path', type=str, help="Path to the graph visualization tool", required=True)
    parser.add_argument('--package-name', type=str, help="Name of the package to analyze", required=True)
    parser.add_argument('--output-file', type=str, help="Path to the output file", required=True)
    parser.add_argument('--max-depth', type=int, help="Maximum depth for dependency analysis", default=3)

    args = parser.parse_args()

    dependencies = get_dependencies(args.package_name, args.max_depth)
    mermaid_code = generate_mermaid(args.package_name, dependencies)

    with open(args.output_file, 'w') as file:
        file.write(mermaid_code)

    print(f"Mermaid code written to {args.output_file}")


if __name__ == "__main__":
    main()

