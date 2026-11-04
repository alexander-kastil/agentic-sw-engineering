import React, { useState, useEffect } from 'react';
import { CatalogItem, CartItem } from '../types';
import './ShopItem.css';

interface ShopItemProps {
  food: CatalogItem;
  inCart: number;
  onAmountChange: (item: CartItem) => void;
}

export const ShopItem: React.FC<ShopItemProps> = ({
  food,
  inCart,
  onAmountChange,
}) => {
  const [quantity, setQuantity] = useState(inCart);

  useEffect(() => {
    setQuantity(inCart);
  }, [inCart]);

  const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const amount = Math.max(0, parseInt(e.target.value, 10) || 0);
    setQuantity(amount);
    onAmountChange({
      id: food.id,
      name: food.name,
      price: food.price,
      quantity: amount,
    });
  };

  const handleIncrement = () => {
    const newQuantity = quantity + 1;
    setQuantity(newQuantity);
    onAmountChange({
      id: food.id,
      name: food.name,
      price: food.price,
      quantity: newQuantity,
    });
  };

  const handleDecrement = () => {
    if (quantity > 0) {
      const newQuantity = quantity - 1;
      setQuantity(newQuantity);
      onAmountChange({
        id: food.id,
        name: food.name,
        price: food.price,
        quantity: newQuantity,
      });
    }
  };

  return (
    <article className={`shop-item${quantity > 0 ? ' in-cart' : ''}`}>
      {food.pictureUrl && (
        <img
          src={`/assets/images/${food.pictureUrl}`}
          alt={food.name}
          className='item-image'
          onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
          }}
        />
      )}
      <div className='text-section'>
        <h2 className='item-title'>{food.name}</h2>
        <p className='description'>{food.description}</p>
      </div>
      <div className='side-section'>
        <span className='price'>{food.price.toFixed(2)} €</span>
        <div
          className='number-picker'
          role='group'
          aria-label={`Quantity of ${food.name}`}
        >
          <button
            type='button'
            onClick={handleDecrement}
            className='picker-btn picker-remove'
            aria-label={`Remove one ${food.name}`}
            disabled={quantity <= 0}
          >
            <span className='material-icons'>remove</span>
          </button>
          <input
            type='number'
            min='0'
            value={quantity}
            onChange={handleQuantityChange}
            className='quantity-input'
            aria-label={`Quantity of ${food.name}`}
          />
          <button
            type='button'
            onClick={handleIncrement}
            className='picker-btn picker-add'
            aria-label={`Add one ${food.name}`}
          >
            <span className='material-icons'>add</span>
          </button>
        </div>
      </div>
    </article>
  );
};
