import { ButtonHTMLAttributes } from 'react';
import './Button.css';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'outline' | 'icon';
  size?: 'small' | 'medium' | 'large';
}

export const Button = ({ 
  children, 
  variant = 'primary',
  size = 'medium',
  className,
  ...props 
}: ButtonProps) => {
  return (
    <button 
      className={`button ${variant} ${size} ${className || ''}`}
      {...props}
    >
      {children}
    </button>
  );
}; 