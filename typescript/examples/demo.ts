// Explicitly include .js extension to satisfy high-level NodeNext module specifications
import { PyJSBridge } from '../src/Bridge.js';

async function runDemo() {
    const bridge = new PyJSBridge();

    bridge.on("open", () => console.log("🚀 Connection verified via Event Emitter!"));
    bridge.on("close", () => console.warn("⚠️ Pipeline disconnected. Triggering auto-reconnect..."));

    try {
        // Asynchronously block thread until bridge channel is active
        await bridge.connect();
        
        // Minor absolute buffer giving handshakes absolute stability
        await new Promise(resolve => setTimeout(resolve, 100));

        console.log("Calling 'basic_add' on Python side...");
        const mathResult = await bridge.call<number>("basic_add",);
        console.log(`Result from Python: ${mathResult}`); // 60

        console.log("\nCalling 'heavy_data_process' on Python side...");
        const mockPayload = { items: ["token_a", "token_b", "token_c"], security_level: "HIGH" };
        
        const processResult = await bridge.call<any>("heavy_data_process", ["usr_9921", mockPayload]);
        console.log("Deep System Response from Python:", JSON.stringify(processResult, null, 2));

    } catch (error) {
        console.error("Critical Execution Interrupted:", error);
    }
}

runDemo();
