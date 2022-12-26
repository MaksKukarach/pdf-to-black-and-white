from pdf2image import convert_from_path
import img2pdf
import cv2
import os

THRESHOLD = 120

def main():
    print()
    print('Welcome!')

    print('First, put your pdf file into "input-files" folder.')
    file_name = input('Then, enter your pdf file name: ')
    print()
    print('[Starting...]')
    if file_name.endswith('.jpg'):
        convert_single_image(file_name)
    else:
        file = convert_from_path(f'Program\input-files\{file_name}', 300)
        convert_pdf2jpg(file)
        apply_binary_to_images()
        convert_images2pdf(result_name=file_name)

    print()
    print('Done! You can now get your file from "output-files" folder.')
    print()


def convert_pdf2jpg(file):
    file_length = len(file)
    for i in range(file_length):
        # The line below makes page numbers zero-padded
        # e.g. page1 -> page1000, page 22 -> page2200
        # This naming is needed because img2pdf sorts page names out in lexicografic ordering before converting them
        zero_padded_i = str(i).rjust(4, '0')
        file[i].save(f'Program\processed-files\page{zero_padded_i}.jpg', 'JPEG')
        print(f'[Pages processed: {int(i)+1}/{file_length}]')
    print('[Successfully converted .pdf to .jpg]')

def convert_images2pdf(result_name: str):
    with open(f'Program\output-files\{result_name}', 'wb') as result:
        pages_list = [f'Program\processed-files\{file}' for file in os.listdir('Program\processed-files')]
        result.write(img2pdf.convert(pages_list))
    # Delete obsolete middle files
    path = 'Program\\processed-files\\'
    for file in os.listdir(path):
        os.remove(path + file)
    print('[Successfully merged the .pdf file]')

def apply_binary_to_images():
    # Apply same binary scale to each file in processed-files folder
    for file_name in os.listdir('Program\processed-files'):
        path = f'Program\processed-files\{file_name}'
        originalImage = cv2.imread(path)
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, THRESHOLD, 255, cv2.THRESH_BINARY)
        index = file_name.replace('.jpg', '').split('page')[1]
        cv2.imwrite(f'Program\processed-files\page{index}.jpg', blackAndWhiteImage)
    print('[Successfully applied black-and-white filter]')

def convert_single_image(file_name):
    path = f'Program\input-files\{file_name}'
    originalImage = cv2.imread(path)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    (thresh, BinaryImage) = cv2.threshold(grayImage, THRESHOLD, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'Program\output-files\{file_name}', BinaryImage)

if __name__ == '__main__':
    main()