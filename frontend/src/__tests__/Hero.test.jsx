import { render, screen, waitFor } from "@testing-library/react";
import Hero from "../components/Hero";

describe("Hero component", () => {
  test("renders headline and subheading", () => {
    render(<Hero />);
    expect(
      screen.getByText("CyberMag: Stay Ahead of Cyber Threats")
    ).toBeInTheDocument();

    expect(
      screen.getByText(
        /We empower digital defenders with timely cyber threat intelligence/i
      )
    ).toBeInTheDocument();
  });

  test("renders the ShieldCheck icon", () => {
    render(<Hero />);
    const icon = screen.getByTestId("shield-icon");
    expect(icon).toBeInTheDocument();
  });

  test("renders the terminal block", () => {
    render(<Hero />);
    const terminal = screen.getByText("cybermag@terminal:~$");
    expect(terminal).toBeInTheDocument();
  });

  test("renders at least one animated terminal line", async () => {
    render(<Hero />);
    await waitFor(() => {
      const lines = screen.getAllByText(/AI|Phishing|Ransomware|Malware/i);
      expect(lines.length).toBeGreaterThan(0);
    }, { timeout: 3000 });
  });
});