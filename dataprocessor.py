import argparse

def remove_duplicate_posts(file_path):
    unique_posts = {}
    processed_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if line.startswith("Title:"):
            title = line
        elif line.startswith("Content:"):
            content = line
        elif line.startswith("Replies:"):
            reply = line

            if content not in unique_posts:
                unique_posts[content] = title
                processed_data.append(title + '\n')
                processed_data.append(content + '\n')
                processed_data.append(reply + '\n')
                processed_data.append("-------\n")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(processed_data)

    return len(unique_posts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file path", type=str, default="posts_data.txt")

    args = parser.parse_args()
    input_file = args.input
    total_posts = remove_duplicate_posts(input_file)

    print(f"Total posts: {total_posts}")

if __name__ == "__main__":
    main()