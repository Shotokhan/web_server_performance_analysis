import os


def gen_random_data(kb_size):
    return os.urandom(1024 * kb_size)


def random_file_given_size(kb_size, filename=None):
    if filename is None:
        filename = str(kb_size) + ".bin"
    with open(filename, 'wb') as f:
        f.write(gen_random_data(kb_size))


def txt_file_given_size(kb_size, filename=None):
    if filename is None:
        filename = str(kb_size) + ".txt"
    with open(filename, 'w') as f:
        f.write("A" * kb_size * 1024)


if __name__ == "__main__":
    kb_sizes = [140, 145, 150, 155, 160]
    for kb_s in kb_sizes:
        random_file_given_size(kb_s)
        txt_file_given_size(kb_s)
