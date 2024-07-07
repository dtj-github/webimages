
import layer2 as l2

def create_html_content(request):
    params = l2.get_params(request)
    images = l2.create_images(params)
    html_content = l2.make_html_content(images)
    return html_content