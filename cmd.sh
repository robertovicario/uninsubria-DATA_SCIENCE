#!/bin/bash

# =========================
# Configurations
# =========================

# Icons
ICON_START="▶"     # U+25B6
ICON_STOP="■"      # U+25A0
ICON_SETUP="⚙"     # U+2699
ICON_DOWNLOAD="↓"  # U+2193
ICON_CLEAN="♻"     # U+267B
ICON_OK="✓"        # U+2713
ICON_ERR="✗"       # U+2717

# Colors
RESET="\033[0m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"

# GCP
PROJECT_ID="uninsubria-data-science"
DATASET_ID="larionow-dataset"
REGION_RUN="europe-west8"
REGION_SCHEDULER="europe-west1"
JOB_NAME="collector"
SCHEDULER_JOB="collector-job"
TIME_ZONE="Europe/Rome"
SERVICE_ACCOUNT="289545143980-compute@developer.gserviceaccount.com"
RUN_ARGS=(
    --image="${REGION_RUN}-docker.pkg.dev/${PROJECT_ID}/${DATASET_ID}/${JOB_NAME}:latest"
    --region="${REGION_RUN}"
    --memory=2Gi
    --cpu=2
    --task-timeout=30m
)
SCHEDULER_ARGS=(
    --location="${REGION_SCHEDULER}"
    --schedule="*/5 * * * *"
    --time-zone="${TIME_ZONE}"
    --uri="https://run.googleapis.com/v2/projects/${PROJECT_ID}/locations/${REGION_RUN}/jobs/${JOB_NAME}:run"
    --http-method=POST
    --oauth-service-account-email="${SERVICE_ACCOUNT}"
    --oauth-token-scope="https://www.googleapis.com/auth/cloud-platform"
)

# =========================
# Methods
# =========================

setup() {

    # Environment
    printer -setup "Setting up the project..."
    uv python install 3.12.10
    uv venv --python 3.12.10

    # Requirements
    uv pip install -r packages/collector.txt
    uv pip install -r packages/notebook.txt

    # Handler
    STATUS=$?
    handler $STATUS
}

collector() {

    # JOB
    printer -start "Starting the data collection..."
    cd jobs || exit 1
    uv run python collector.py
    cd - >/dev/null || exit 1

    # Handler
    STATUS=$?
    handler $STATUS
}

schedule_jobs() {

    printer -setup "Scheduling jobs with Google Cloud Scheduler..."
    if gcloud scheduler jobs describe "${SCHEDULER_JOB}" \
        --location="${REGION_SCHEDULER}" >/dev/null 2>&1; then

        # UPDATE
        gcloud scheduler jobs update http "${SCHEDULER_JOB}" \
            "${SCHEDULER_ARGS[@]}" || {
            handler $?
            return
        }

        # RESUME
        STATE=$(gcloud scheduler jobs describe "${SCHEDULER_JOB}" \
            --location="${REGION_SCHEDULER}" \
            --format="value(state)")
        if [ "${STATE}" = "PAUSED" ]; then
            gcloud scheduler jobs resume "${SCHEDULER_JOB}" \
                --location="${REGION_SCHEDULER}"
        fi
    else

        # CREATE
        gcloud scheduler jobs create http "${SCHEDULER_JOB}" \
            "${SCHEDULER_ARGS[@]}"
    fi

    # Handler
    handler $?
}

deploy_jobs() {

    # BUILD
    printer -setup "Deploying jobs on Google Cloud Run..."
    gcloud builds submit --config cloudbuild.yaml . || {
        handler $?
        return
    }

    # DEPLOY
    gcloud run jobs deploy "${JOB_NAME}" \
        "${RUN_ARGS[@]}"

    # Handler
    handler $?
}

# =========================
# Handlers
# =========================

usage() {
    cat <<EOF

1. Usage:
    - bash $0 <command>

2. Commands:
    - [${ICON_SETUP}] setup
    - [${ICON_START}] collector
    - [${ICON_SETUP}] schedule_jobs
    - [${ICON_SETUP}] deploy_jobs

EOF
    exit 1
}

printer() {
    local STATUS="$1"
    local MESSAGE="$2"
    local ICON=""
    local COLOR=""
    case "$STATUS" in
        -start)
            ICON="$ICON_START"
            COLOR="$BLUE"
            ;;
        -stop)
            ICON="$ICON_STOP"
            COLOR="$RED"
            ;;
        -debug)
            ICON="$ICON_START"
            COLOR="$CYAN"
            ;;
        -setup)
            ICON="$ICON_SETUP"
            COLOR="$MAGENTA"
            ;;
        -clean)
            ICON="$ICON_CLEAN"
            COLOR="$YELLOW"
            ;;
        -success)
            ICON="$ICON_OK"
            COLOR="$GREEN"
            ;;
        -error)
            ICON="$ICON_ERR"
            COLOR="$RED"
            ;;
        *)
            ICON="$ICON_ERR"
            COLOR="$RED"
            ;;
    esac
    echo ""
    echo -e "${COLOR}[${ICON}] ${MESSAGE}${RESET}"
    echo ""
}

handler() {
    local STATUS=$1
    if [ $STATUS -eq 0 ]; then
        printer -success "Process completed successfully"
    else
        printer -error "An unexpected error occurred"
        exit 1
    fi
}

case $1 in
    setup)
        setup
        ;;
    collector)
        collector
        ;;
    schedule_jobs)
        schedule_jobs
        ;;
    deploy_jobs)
        deploy_jobs
        ;;
    *)
        usage
        ;;
esac
