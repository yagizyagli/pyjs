import { PyJSBridge } from '../src/Bridge';

async function runDemo() {
    // Instantiate the resilient bridge client
    const bridge = new PyJSBridge("localhost", 8765);

    // Setup framework lifecycle event listeners
    bridge.on("open", () => console.log("🚀 Connection verified via Event Emitter!"));
    bridge.on("close", () => console.warn("⚠️ Pipeline disconnected. Triggering auto-reconnect..."));

    try {
        // Connect to the Python backbone server
        await bridge.connect();

        // Execution 1: Trigger the synchronous math function
        console.log("Calling 'basic_add' on Python side...");
        const mathResult = await bridge.call<number>("basic_add", [25, 35]);
        console.log(`Result from Python: ${mathResult}`); // Should log 60

        // Execution 2: Trigger the complex asynchronous engine with dictionary payloads
        console.log("\nCalling 'heavy_data_process' on Python side...");
        const mockPayload = { items: ["token_a", "token_b", "token_c"], security_level: "HIGH" };
        
        const processResult = await bridge.call<any>("heavy_data_process", ["usr_9921", mockPayload]);
        console.log("Deep System Response from Python:", JSON.stringify(processResult, null, 2));

    } catch (error) {
        console.error("Critical Execution Interrupted:", error);
    }
}

runDemo();
