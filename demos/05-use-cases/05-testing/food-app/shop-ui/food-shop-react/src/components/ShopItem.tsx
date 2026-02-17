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
    <div className='shop-item'>
      <div className='item-header'>
        <h3>
          {food.name} - {food.price.toFixed(2)} €
        </h3>
      </div>
      <div className='item-content'>
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
          <p className='description'>{food.description}</p>
        </div>
        <div className='controls-section'>
          <button onClick={handleDecrement} className='icon-btn' title='Remove'>
            ⊖
          </button>
          <input
            type='number'
            min='0'
            value={quantity}
            onChange={handleQuantityChange}
            className='quantity-input'
          />
          <button onClick={handleIncrement} className='icon-btn' title='Add'>
            ⊕
          </button>
        </div>
      </div>
    </div>
  );
};
