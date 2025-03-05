import json
import time
from django.views.generic import TemplateView
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from mirascope.core import groq

@groq.call("llama-3.3-70b-versatile", stream=True)
def joke_explainer(joke: str) -> groq.GroqDynamicConfig:
    """
    Generates a brief explanation of a given joke in a dry but slightly humorous tone.

    Args:
        joke (str): The joke that needs to be explained.

    Returns:
        groq.GroqDynamicConfig: A dynamic configuration object containing the 
        messages formatted for the model, with the user's prompt for explanation.
    """
    prompt = f"Explain very briefly in a dry but slighly humorous tone: {joke}"
    return {"messages": [{"role": "user", "content": prompt}]}


class IndexView(TemplateView):
    """
    A view that handles the index page for the joke explainer application.
    It extends the TemplateView to render a specific template and handle
    POST requests for joke explanations.
    """
    template_name = 'joke_explainer/index.html'

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        """
        Dispatches the request to the appropriate handler based on the HTTP method.
        
        If the request method is POST, it calls the post method to handle the request.
        Otherwise, it calls the superclass's dispatch method.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response object returned by the appropriate handler.
        """
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        """
        Handles POST requests to process a joke and return a streaming response
        with the explanation.

        It expects a JSON body containing a 'joke' key. If the JSON is valid,
        it processes the joke and returns a streaming HTTP response. If the JSON
        is invalid or an error occurs during processing, it returns an appropriate
        JSON error response.

        Args:
            request: The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            StreamingHttpResponse or JsonResponse: The response containing the joke
            explanation or an error message.
        """
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            joke = body_data.get('joke', '')
        
            def stream_response():
                """
                A generator function that streams the response chunks for the joke
                explanation, yielding each chunk with a delay.

                Yields:
                    str: The next chunk of the joke explanation.
                """
                stream = joke_explainer(joke)
                for chunk, _ in stream:
                    yield chunk
                    time.sleep(0.15)

            return StreamingHttpResponse(stream_response(), content_type='text/html')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)