import { Navigation } from "@/components/Navigation";
import { HeroSection } from "@/components/HeroSection";
import { DemoSection } from "@/components/DemoSection";
import { ContactSection } from "@/components/ContactSection";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navigation />
      <HeroSection />
      <DemoSection />
      <ContactSection />
    </div>
  );
};

export default Index;
