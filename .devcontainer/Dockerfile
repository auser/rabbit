FROM python:3.11-slim

# Install uv, zsh, git, curl, sudo, and oh-my-zsh dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        zsh git curl ca-certificates locales sudo \
    && pip install uv \
    && rm -rf /var/lib/apt/lists/*

# Set up locale (for oh-my-zsh)
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Add vscode group and user, create home directory
RUN groupadd -r vscode \
    && useradd -r -g vscode -d /home/vscode -s /usr/bin/zsh -m vscode

# Allow vscode user passwordless sudo
RUN echo 'vscode ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-vscode \
    && chmod 0440 /etc/sudoers.d/90-vscode

# Install oh-my-zsh and plugins for vscode user
RUN curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -o /tmp/install.sh

RUN RUNZSH=no CHSH=no KEEP_ZSHRC=yes sh /tmp/install.sh \
    && git clone https://github.com/zsh-users/zsh-autosuggestions /home/vscode/.oh-my-zsh/custom/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting /home/vscode/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting \
    && rm /tmp/install.sh

# Add a great .zshrc for vscode user
COPY --chown=vscode:vscode .devcontainer/zshrc /home/vscode/.zshrc

WORKDIR /workspace

COPY ../uv.lock ../pyproject.toml ./

RUN uv pip install -r requirements.txt || true

CMD ["zsh"] 