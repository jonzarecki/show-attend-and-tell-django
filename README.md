# Show, Attend and Tell on a django server

![Alt text](https://github.com/yunjey/show-attend-and-tell/raw/master/jpg/attention_over_time.jpg "Soft attention")


## References

Author's theano code: https://github.com/kelvinxu/arctic-captions

Original tensorflow implementation: https://github.com/yunjey/show-attend-and-tell

Original django file upload server implementation: https://github.com/sibtc/simple-file-upload

<br/>


### Prerequisites

First, clone this repo.

```bash
$ git clone https://github.com/yonilx/show-attend-and-tell-django.git
```

Install all required packages.

Run the django server with:

```bash
$ python manage.py migrate
$ python manage.py runserver
```

The project is able to upload new images and show their result using the soft attention model in "Show, Attend and tell".
