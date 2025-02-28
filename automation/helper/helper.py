import os



def log_function_name(func):
    def wrapper(*args, **kwargs):
        print(f"Running function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log_function_name
def get_page_source(driver, filename):
    # Get the HTML source of the current page
    html_source = driver.page_source

    # Create a directory to store the HTML files if it doesn't exist
    if not os.path.exists('html_files'):
        os.makedirs('html_files')

    # Write the HTML source to a file
    with open(f'html_files/{filename}.html', 'w') as file:
        file.write(html_source)

