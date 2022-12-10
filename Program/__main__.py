from pdf2image import convert_from_path
import cv2
import img2pdf

def convert_pdf2jpg(pages):
    file_length = len(pages)
    for i in range(file_length):
        # Save pages as images
        pages[i].save(f'Program\processed-files\page{i}.jpg', 'JPEG')
        print(f'[Pages processed: {i+1}/{file_length}]')
    print('[Successfully converted .pdf to .jpg]')

def convert_images2pdf(file_length: int, result_name: str):
    with open(f'Program\output-files\{result_name}', 'wb') as result:
        pages_list = [f'Program\processed files\page{i}.jpg' for i in range(file_length)]
        result.write(img2pdf.convert(pages_list.encode()))
    print('[Successfully merged the .pdf file]')

def apply_binary_to_images(file_length: int):
    for i in range(file_length):
        path = f'Program\processed-files\page{i}.jpg'
        originalImage = cv2.imread(path)
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 20, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f'processed-files\page{i}.jpg', blackAndWhiteImage)
    print('[Successfully applied black-and-white filter]')

def get_file_name():
    print('First, put your pdf file into "input-files" folder.')
    # file_name = input('Then, enter your pdf file name: ')
    file_name = 'sample'
    if not file_name.endswith('.pdf'):
       file_name += '.pdf'
    return file_name

def main():
    print('With this tool you can easily convert your pdf to black-and-white binary (not grayscale)')

    file_name = get_file_name()
    print('[Starting...]')

    input_path = f'Program\input-files\{file_name}'
    # extract pdf from input_path with a certain dpi
    file = convert_from_path(input_path, 300)
    file_length = len(file)

    convert_pdf2jpg(file)
    apply_binary_to_images(file_length=file_length)
    convert_images2pdf(file_length=file_length, result_name=file_name)

    print()
    print('Done! You can now get your file from "output-files" folder.')

if __name__ == '__main__':
    main()