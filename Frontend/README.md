#### This is the folder of frontend

# Vue 3 + Vite + Shadcn

###### Note :
 - Make sure to run frontend you have node v20.18.3 npm 10.8.2 

### :star: Steps to run the frontend

#### Clone the repo
```bash
#for https

git clone https://github.com/Delvin-V/soft-engg-project-jan-2025-se-Jan-37.git

#for ssh

git clone git@github.com:Delvin-V/soft-engg-project-jan-2025-se-Jan-37.git   
```

#### Navigate to projects folder
```bash
cd soft-engg-project-jan-2025-se-Jan-37
```

#### Switch to [] branch to see frontend
```bash
git switch -c backend-setup origin/backend-setup
```

#### Navigate to frontend folder
```bash
cd Frontend
```

#### Install required dependencies
```bash
npm install
```

### Now to Run the server
```bash
npm run dev
```


### :star: Steps to use shadcn ui

- To use any component from [shadcn ui](https://www.shadcn-vue.com/docs/components/sidebar.html)

    - Install that component using `npx shadcn-vue@latest add <component name>`
    - This will be installed in src/components/ui
    - Now you can see in docs how to use that
    - A demmo of using `Button` component You can see, i implemented that
    - `<script setup lang="ts">` remove this `lang="ts"` when you use new component
    - make sure that you should not edit manually anything in src/components/ui because in this folder all the dependencies of shadcn UI will install automatically. when you run the command `npx shadcn-vue@latest add <component name>`


### For better experience and suggestion install these extentions in vscode
 - Tailwind CSS IntelliSense
 - Vue - Official


