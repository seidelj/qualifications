# Example for Managing Qualifications on Mturk using oTree

The qualification app assigns an Mturk qualification to subjects who agree to participate (defined as `_PREQUAL` in setting.py).  See the `before_next_page` method defined in the Qualification class under qualification/pages.py.

The payment_info app assigns a qualification to prevent mturkers from participating twice (defined as `_AMK1` in settings.py).  See the `before_next_page` method in 
the PaymentInfo class under payment_info/pages.py.
