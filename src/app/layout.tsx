import type { Metadata } from "next";
import "./globals.css";
import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";

export const metadata: Metadata = {
	title: "Resume Generator | Create Professional Resumes Online",
	description:
		"Create professional resumes online with our free resume builder. Generate modern, professional resumes in minutes.",
	keywords:
		"resume generator, professional resume, online resume builder, create resume, job application, career",
	robots: "index, follow",
	openGraph: {
		title: "Resume Generator | Create Professional Resumes Online",
		description: "Create professional resumes online with our free resume builder. Generate modern, professional resumes in minutes.",
		url: "https://evlilikhazirligi.com",
		type: "website",
		locale: "en_US",
		siteName: "Resume Generator",
	},
	twitter: {
		card: "summary_large_image",
		title: "Resume Generator | Create Professional Resumes Online",
		description: "Create professional resumes online with our free resume builder. Generate modern, professional resumes in minutes.",
	},
	authors: [{ name: "Chris Evelds", url: "https://evlilikhazirligi.com" }],
	creator: "Chris Evelds",
	publisher: "Maria",
	themeColor: [
		{ media: "(prefers-color-scheme: light)", color: "white" },
		{ media: "(prefers-color-scheme: dark)", color: "black" },
	],
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang='en'>
			<head suppressHydrationWarning>
				{/* Google Search Console Verification */}
				<meta name="google-site-verification" content="YOUR_GOOGLE_SEARCH_CONSOLE_CODE" />

				{/* Google Analytics */}
				<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_ANALYTICS_ID"></script>
				<script dangerouslySetInnerHTML={{
					__html: `
						window.dataLayer = window.dataLayer || [];
						function gtag(){dataLayer.push(arguments);}
						gtag('js', new Date());
						gtag('config', 'YOUR_ANALYTICS_ID');
					`
				}} />

				{/* Google AdSense */}
				<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3139769263752872" crossOrigin="anonymous"></script>

				{/* Additional SEO Meta Tags */}
				<meta name="viewport" content="width=device-width, initial-scale=1.0" />
				<meta name="language" content="en" />
				<meta name="author" content="Your Name" />
				<meta name="copyright" content=" 2025 Your Name" />
				<meta name="rating" content="General" />
				<meta name="revisit-after" content="7 days" />
				<meta name="distribution" content="global" />
				<meta name="resource-type" content="document" />
				<meta name="google-adsense-account" content="ca-pub-3139769263752872">
			</head>
			<body suppressHydrationWarning>
				<Navigation />
				{children}
				<Footer />
			</body>
		</html>
	);
}
