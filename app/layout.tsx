import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Galaxy Holding | ERPNext + n8n + IA',
  description:
    'Implementación integral de ERPNext, n8n y automatización con IA para la estructura empresarial Galaxy Holding.',
  metadataBase: new URL('https://galaxy-holding.vercel.app'),
  openGraph: {
    title: 'Galaxy Holding - Ecosistema ERP Inteligente',
    description:
      'Arquitectura completa de ERPNext, n8n y herramientas de IA para una operación empresarial multi-dominio.',
    url: 'https://galaxy-holding.vercel.app',
    siteName: 'Galaxy Holding',
    locale: 'es_ES',
    type: 'website'
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Galaxy Holding | ERPNext + n8n + IA',
    description:
      'Automatización empresarial inteligente con ERPNext, n8n y asistentes de IA especializados.'
  }
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
