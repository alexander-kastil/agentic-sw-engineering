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
    const amount = parseInt(e.target.value, 10);
    setQuantity(amount);

    const cartItem: CartItem = {
      id: food.id,
      name: food.name,
      price: food.price,
      quantity: amount,
    };
    onAmountChange(cartItem);
  };

  const handleIncrement = () => {
    const newQuantity = quantity + 1;
    setQuantity(newQuantity);

    const cartItem: CartItem = {
      id: food.id,
      name: food.name,
      price: food.price,
      quantity: newQuantity,
    };
    onAmountChange(cartItem);
  };

  const handleDecrement = () => {
    if (quantity > 0) {
      const newQuantity = quantity - 1;
      setQuantity(newQuantity);

      const cartItem: CartItem = {
        id: food.id,
        name: food.name,
        price: food.price,
        quantity: newQuantity,
      };
      onAmountChange(cartItem);
    }
  };

  return (
    <div className='shop-item'>
      <div className='item-card'>
        <div className='item-header'>
          <h3>{food.name}</h3>
          <span className='price'>€{food.price.toFixed(2)}</span>
        </div>
        <div className='item-content'>
          {food.pictureUrl && (
            <div className='image-container'>
              <img
                src={`assets/images/${food.pictureUrl}`}
                alt={food.name}
                onError={(e) => {
                  (e.target as HTMLImageElement).src =
                    'assets/images/placeholder.png';
                }}
              />
            </div>
          )}
          <div className='description'>{food.description}</div>
          <div className='quantity-controls'>
            <button onClick={handleDecrement} className='btn'>
              −
            </button>
            <input
              type='number'
              min='0'
              value={quantity}
              onChange={handleQuantityChange}
              className='quantity-input'
            />
            <button onClick={handleIncrement} className='btn'>
              +
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
