/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    optimizeCss: true,
    outputFileTracingIncludes: {
      '/app/docs/[slug]/route': ['./docs/**/*']
    }
  }
};

module.exports = nextConfig;
