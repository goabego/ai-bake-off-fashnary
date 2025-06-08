import { ProductDisplay } from '@/types/product';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface ProductCardProps {
  product: ProductDisplay;
}

export function ProductCard({ product }: ProductCardProps) {
  const getStockStatusColor = (status: string) => {
    switch (status) {
      case 'Out of Stock':
        return 'destructive';
      case 'Low Stock':
        return 'warning';
      default:
        return 'success';
    }
  };

  return (
    <Card className="overflow-hidden">
      <div className="aspect-square relative">
        <img
          src={product.image}
          alt={product.description}
          className="object-cover w-full h-full"
        />
      </div>
      <CardHeader>
        <CardTitle className="line-clamp-2">{product.description}</CardTitle>
        <CardDescription>
          {product.type} - {product.color}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-2xl font-bold">{product.price}</span>
            <Badge variant={getStockStatusColor(product.stock_status)}>
              {product.stock_status}
            </Badge>
          </div>
          <p className="text-sm text-muted-foreground">
            Graphic: {product.graphic}
          </p>
          <p className="text-sm text-muted-foreground">
            Variant: {product.variant}
          </p>
        </div>
      </CardContent>
    </Card>
  );
} 