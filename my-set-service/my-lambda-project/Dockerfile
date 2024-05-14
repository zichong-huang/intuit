# Use the base image provided by AWS for Lambda that includes Python 3.8
FROM public.ecr.aws/lambda/python:3.8

# Copy your function code and requirements file into the image
COPY src/lambda_function.py ${LAMBDA_TASK_ROOT}/
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install any dependencies
RUN python3.8 -m pip install -r requirements.txt --no-cache-dir

# Set the CMD to your handler (could be already set by the base image)
CMD ["lambda_function.lambda_handler"]
