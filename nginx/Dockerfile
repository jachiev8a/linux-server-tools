FROM nginx:1.18

# alias in case of interact with container easier to do ll
RUN echo 'alias ll="ls -althF --color=auto"' >> ~/.bashrc

# nginx config for container.
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY os-monitor-app.conf /etc/nginx/conf.d/
