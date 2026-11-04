import React, { useState } from 'react';
import { CartItem } from '../types';
import './CheckoutModal.css';

interface CheckoutModalProps {
  items: CartItem[];
  total: number;
  onClose: () => void;
  onConfirmed: () => void;
}

interface CheckoutFormValues {
  name: string;
  email: string;
  phone: string;
  street: string;
  zipCode: string;
  city: string;
  country: string;
  paymentType: string;
  accountNumber: string;
}

const mockOrder: CheckoutFormValues = {
  name: 'Giro Kastil',
  email: 'giro.kastil@integrations.at',
  phone: '+43 664 436 07 77',
  street: 'Himmelstraße 115',
  zipCode: '1190',
  city: 'Wien',
  country: 'Austria',
  paymentType: 'Bank Account',
  accountNumber: '1234',
};

const fieldLabels: Record<keyof CheckoutFormValues, string> = {
  name: 'Name',
  email: 'E-Mail',
  phone: 'Phone',
  street: 'Street',
  zipCode: 'Zip Code',
  city: 'City',
  country: 'Country',
  paymentType: 'Payment Type',
  accountNumber: 'Account Number',
};

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const validate = (
  values: CheckoutFormValues,
): Partial<Record<keyof CheckoutFormValues, string>> => {
  const errors: Partial<Record<keyof CheckoutFormValues, string>> = {};
  (Object.keys(values) as (keyof CheckoutFormValues)[]).forEach((key) => {
    if (!values[key].trim()) {
      errors[key] = `${fieldLabels[key]} is required`;
    }
  });
  if (!errors.email && !emailPattern.test(values.email)) {
    errors.email = 'Enter a valid email address';
  }
  return errors;
};

const createOrderId = (): string =>
  `ORD-${Date.now().toString(36).toUpperCase()}-${Math.floor(Math.random() * 1000)
    .toString()
    .padStart(3, '0')}`;

export const CheckoutModal: React.FC<CheckoutModalProps> = ({
  items,
  total,
  onClose,
  onConfirmed,
}) => {
  const [values, setValues] = useState<CheckoutFormValues>(mockOrder);
  const [submitted, setSubmitted] = useState(false);
  const [orderId, setOrderId] = useState<string | null>(null);

  const errors = validate(values);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitted(true);
    if (Object.keys(validate(values)).length === 0) {
      setOrderId(createOrderId());
    }
  };

  const renderField = (name: keyof CheckoutFormValues) => (
    <label className='checkout-field'>
      <span>{fieldLabels[name]}</span>
      <input
        name={name}
        value={values[name]}
        onChange={handleChange}
        className={submitted && errors[name] ? 'invalid' : ''}
      />
      {submitted && errors[name] && (
        <span className='field-error'>{errors[name]}</span>
      )}
    </label>
  );

  if (orderId) {
    return (
      <div className='checkout-backdrop'>
        <div className='checkout-modal confirmation'>
          <h2>Your order was submitted</h2>
          <p>Thank you for your order!</p>
          <p className='order-id'>Your order number is {orderId}</p>
          <p>We will let you know after your payment was processed</p>
          <button type='button' className='primary-btn' onClick={onConfirmed}>
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className='checkout-backdrop'>
      <div className='checkout-modal'>
        <header className='checkout-header'>
          <h2>Checkout</h2>
          <button
            type='button'
            className='close-btn'
            onClick={onClose}
            aria-label='Close checkout'
          >
            ×
          </button>
        </header>
        <form onSubmit={handleSubmit} noValidate>
          <fieldset>
            <legend>Customer</legend>
            {renderField('name')}
            {renderField('email')}
            {renderField('phone')}
          </fieldset>
          <fieldset>
            <legend>Shipping Address</legend>
            {renderField('street')}
            {renderField('zipCode')}
            {renderField('city')}
            {renderField('country')}
          </fieldset>
          <fieldset>
            <legend>Payment</legend>
            {renderField('paymentType')}
            {renderField('accountNumber')}
          </fieldset>
          <fieldset>
            <legend>Items</legend>
            <ul className='checkout-items'>
              {items.map((item) => (
                <li key={item.id}>
                  <span className='item-quantity'>{item.quantity} ×</span>
                  <span className='item-name'>{item.name}</span>
                  <span className='item-price'>
                    €{(item.price * item.quantity).toFixed(2)}
                  </span>
                </li>
              ))}
            </ul>
            <div className='checkout-total'>Total: €{total.toFixed(2)}</div>
          </fieldset>
          <div className='checkout-actions'>
            <button type='button' className='secondary-btn' onClick={onClose}>
              Cancel
            </button>
            <button type='submit' className='primary-btn'>
              Complete Checkout
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
