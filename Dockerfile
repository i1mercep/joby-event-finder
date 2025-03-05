FROM python:3.13-slim-bookworm AS builder
ARG PIP_REQUIREMENTS_FILE=requirements_dev.txt
COPY $PIP_REQUIREMENTS_FILE .
# Install required packages
RUN apt-get update && apt-get install --no-install-recommends -y curl gettext-base xz-utils
# RUN pip install --upgrade pip setuptools && pip install --no-deps -r $PIP_REQUIREMENTS_FILE
# Create virtualenv
RUN python -m venv /venv && /venv/bin/pip install -U pip
# Build and install
RUN /venv/bin/pip install --no-deps --no-cache-dir -q -r "$PIP_REQUIREMENTS_FILE"
# Download and unpack watchexec
RUN curl -L -s https://github.com/watchexec/watchexec/releases/download/v2.3.0/watchexec-2.3.0-x86_64-unknown-linux-musl.tar.xz \
    --output - | tar -xJf - --strip-components=1 -C /usr/bin/ watchexec-2.3.0-x86_64-unknown-linux-musl/watchexec


FROM python:3.13-slim-bookworm AS run-stage
ARG PIP_REQUIREMENTS_FILE=requirements_dev.txt
ARG APP_DIR="/app"
WORKDIR ${APP_DIR}

# Copy the required app files from local directory
COPY ./src ${APP_DIR}/src/
COPY ./tests ${APP_DIR}/tests/
COPY ./scripts ${APP_DIR}/scripts/
COPY pyproject.toml ${APP_DIR}/
COPY alembic.ini ${APP_DIR}/

# Copy from builder
COPY --from=builder /root/.cache /root/.cache
COPY --from=builder /venv /venv
COPY --from=builder /usr/bin/watchexec /usr/bin/watchexec
COPY --from=builder /usr/bin/envsubst /usr/bin/envsubst

RUN apt-get update && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*
