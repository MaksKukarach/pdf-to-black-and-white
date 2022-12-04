from pdf2image import convert_from_path
import cv2
import img2pdf
# from fpdf import FPDF

def convert_pdf2jpg(pages):
    file_length = len(pages)
    for i in range(file_length):
        # Save pages as images
        pages[i].save(f'processed-files\page{i}.jpg', 'JPEG')
        print(f'[Pages processed: {i+1}/{file_length}]')
    
    print('[Successfully converted .pdf to .jpg]')

# convert using img2pdf
def convert_img2pdf(file_length: int, output_name='result',input_folder='processed-files'):
    with open(f'output-files\{output_name}', 'wb') as output_file:
        pages_list = [f'{input_folder}\page{i}.jpg' for i in range(file_length)]
        output_file.write(img2pdf.convert(pages_list))
    
    print('[Successfully merged the .pdf file]')

# convert using fpdf. decide later which way is better
# def convert_img2pdf(file_length: int, input_folder='processed-files'):
#     pdf = FPDF()
#     list_of_images = [f'{input_folder}\page{i}.jpg' for i in range(file_length)]
#     for image in list_of_images:
#         pdf.add_page()
#         pdf.image(image)
#     pdf.output('output-files\output.pdf', 'F')
    
#     print('[Successfully merged the .pdf file]')

def convert_images_to_black_and_white(file_length: int, input_folder='processed-files'):
    for i in range(file_length):
        path = f'{input_folder}/page{i}.jpg'
        originalImage = cv2.imread(path)
        grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 155, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f'processed-files/page{i}.jpg', blackAndWhiteImage)
    
    print('[Successfully applied black-and-white filter]')


def get_file_name():
    print('First, put your pdf file into "input-files" folder.')
    file_name = input('Then, enter your pdf file name: ')
    if not file_name.endswith('.pdf'):
       file_name += '.pdf'
    return file_name

def main():
    print('With this tool you can easily convert your pdf to black-and-white binary (not grayscale)')
    #print('This is particularly useful if you need to get rid of watermarks.')

    file_name = get_file_name()
    print('[Starting...]')

    input_path = f'input-files\{file_name}'
    # extract pdf from input_path with a certain dpi
    input_file = convert_from_path(input_path, 300)
    file_length = len(input_file)

    
    convert_pdf2jpg(input_file)
    convert_images_to_black_and_white(file_length=file_length)
    convert_img2pdf(file_length=file_length, output_name=file_name)

    print('Done! You can now get your file from "output-files" folder.')

if __name__ == '__main__':
    main()