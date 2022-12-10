from pdf2image import convert_from_path
import cv2
import img2pdf
import os

def main():
    print('With this tool you can easily convert your pdf to black-and-white binary (not grayscale)')

    file_name = get_file_name()
    print('[Starting...]')

    input_path = f'Program\input-files\{file_name}'
    # extract pdf from input_path with a certain dpi
    file = convert_from_path(input_path, 300)

    convert_pdf2jpg(file)
    apply_binary_to_images()
    convert_images2pdf(result_name=file_name)

    print()
    print('Done! You can now get your file from "output-files" folder.')

def convert_pdf2jpg(pages):
    file_length = len(pages)
    for i in range(file_length):
        # Save pages as images
        pages[i].save(f'Program\processed-files\page{i}.jpg', 'JPEG')
        print(f'[Pages processed: {i+1}/{file_length}]')
    print('[Successfully converted .pdf to .jpg]')

def convert_images2pdf(result_name: str):
    with open(f'Program\output-files\{result_name}', 'wb') as result:
        pages_list = [f'Program\processed-files\{file}' for file in os.listdir('Program\processed-files')]
        result.write(img2pdf.convert(pages_list))
    print('[Successfully merged the .pdf file]')

def apply_binary_to_images():
    # apply same binary scale to each file in processed-files folder
    for i, file in enumerate(os.listdir('Program\processed-files')):
        path = f'Program\processed-files\{file}'

        originalImage = cv2.imread(path)
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 155, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f'Program\processed-files\page{i}.jpg', blackAndWhiteImage)
    print('[Successfully applied black-and-white filter]')

def get_file_name():
    print('First, put your pdf file into "input-files" folder.')
    file_name = input('Then, enter your pdf file name: ')
    if not file_name.endswith('.pdf'):
       file_name += '.pdf'
    return file_name

if __name__ == '__main__':
    main()