const { execSync } = require('child_process');
const fs = require('fs');

const iterations = 1000;
const artifactPath = './dlx-ref/test-vectors/artifacts/valid_governance_artifact.json';

console.log(`Starting benchmark: ${iterations} verifications of ${artifactPath}...`);

const start = Date.now();

for (let i = 0; i < iterations; i++) {
    // Вызываем CLI для верификации. В реальной системе это был бы вызов библиотеки, 
    // что было бы в 10-100 раз быстрее из-за отсутствия оверхеда на запуск процесса.
    execSync(`node dlx-ref/cli.js verify ${artifactPath} > /dev/null`);
}

const end = Date.now();
const totalTime = (end - start) / 1000;
const tps = iterations / totalTime;

console.log(`--- Benchmark Results ---`);
console.log(`Total time: ${totalTime.toFixed(2)}s`);
console.log(`Throughput (CLI overhead included): ${tps.toFixed(2)} decisions/sec`);
console.log(`Approximate raw execution (assuming 90% CLI overhead): ${(tps * 10).toFixed(0)} decisions/sec`);
