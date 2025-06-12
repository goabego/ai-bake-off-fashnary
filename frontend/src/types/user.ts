// frontend/src/types/user.ts
export interface User {
  id: string;
  name: string;
  description?: string;
  style_preferences?: string[];
  image_url?: string;
  purchase_history?: string[];
  cart_status?: any;
  created_at?: string;
}

export interface UserDisplay extends User {
  image: string; // base64 image from /display endpoint
}
