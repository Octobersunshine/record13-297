import json
import sys


def format_json(data, mode='pretty', indent=2):
    if mode == 'pretty':
        return json.dumps(data, indent=indent, ensure_ascii=False)
    elif mode == 'compact':
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'pretty' or 'compact'.")


def format_json_string(json_str, mode='pretty', indent=2):
    data = json.loads(json_str)
    return format_json(data, mode=mode, indent=indent)


def format_file(input_path, output_path=None, mode='pretty', indent=2):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = format_json(data, mode=mode, indent=indent)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        return output_path
    else:
        print(result)
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(description='JSON Formatter - beautify or compact JSON')
    parser.add_argument('-i', '--input', help='Input JSON file path')
    parser.add_argument('-o', '--output', help='Output file path (optional, prints to stdout if not set)')
    parser.add_argument('-m', '--mode', choices=['pretty', 'compact'], default='pretty',
                        help='Format mode: pretty (indented) or compact (no spaces)')
    parser.add_argument('--indent', type=int, default=2, help='Indentation spaces for pretty mode (default: 2)')
    parser.add_argument('-s', '--string', help='JSON string to format directly')

    args = parser.parse_args()

    try:
        if args.string:
            result = format_json_string(args.string, mode=args.mode, indent=args.indent)
            print(result)
        elif args.input:
            format_file(args.input, args.output, mode=args.mode, indent=args.indent)
        else:
            if sys.stdin.isatty():
                parser.print_help()
                sys.exit(1)
            json_str = sys.stdin.read()
            result = format_json_string(json_str, mode=args.mode, indent=args.indent)
            print(result)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
