#FLASK API :) 
- [virtual env instructions](https://github.com/reed-college/2016_sds_lesson_notes/blob/master/lesson_03_beginning_development.markdown)
- [stripe API flask guide](https://stripe.com/docs/checkout/flask)
- *make and activate virtualenv*
- `pip freeze` (make sure you have python3.6, flask, stripe, virtualenv, virtualenvwrapper)
- `cd /tmp && mkdir venv-demo && cd venv-demo
                virtualenv .`
- `source bin/activate
                which python` 
- once in virtualenv, do:
- 'sudo pip install --upgrade stripe
sudo pip install flask' 
- in terminal, do: `export STRIPE_LOG=debug`
- when running it, be in *activated* venv
- copy and paste this code to terminal:
`PUBLISHABLE_KEY=pk_test_6pRNASCoBOKtIshFeQd4XMUh SECRET_KEY=sk_test_BQokikJOvBiI2HlWgH4olfQ2 python app.py`
- if that doesn't work, try:
`pip install --upgrade stripe`
- if you are still having trouble, double check everything through [stripe python github docs](https://github.com/stripe/stripe-python)