import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import { join } from 'path';

export const runtime = 'nodejs';

const ALLOWED_SLUGS = new Map([
  ['galaxy_master_document', 'galaxy_master_document.md']
]);

const DOCS_DIR = join(process.cwd(), 'docs');

export async function GET(
  _request: Request,
  { params }: { params: { slug: string } }
) {
  const rawSlug = params.slug;
  const fileName = ALLOWED_SLUGS.get(rawSlug);

  if (!fileName) {
    return NextResponse.json(
      {
        error: 'Documento no encontrado',
        slug: rawSlug
      },
      { status: 404 }
    );
  }

  const filePath = join(DOCS_DIR, fileName);

  try {
    const fileBuffer = await fs.readFile(filePath);

    return new NextResponse(fileBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'text/markdown; charset=utf-8',
        'Content-Length': fileBuffer.byteLength.toString(),
        'Content-Disposition': `attachment; filename="${fileName}"`,
        'Cache-Control': 'public, max-age=300'
      }
    });
  } catch (error) {
    console.error(`Error al leer el documento ${fileName}:`, error);
    return NextResponse.json(
      {
        error: 'Documento no encontrado',
        slug: rawSlug
      },
      { status: 404 }
    );
  }
}
